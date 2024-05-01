"""inference_algorithms.py: File containing entailment algorithms."""

from expr import Expr, is_symbol, get_symbols, is_prop_symbol
from utils import extend
from typing import Union
from collections import defaultdict
from cnf import conjuncts

fc_symbols = set()
bc_symbols = []
symbol_list = set()


def tt_entails(kb: 'Expr', query: 'Expr'):
    """A truth table enumeration algorithm for deciding propositional entailment."""
    model_count = [0]  # single element array so I can pass it as a reference
    symbols = list(get_symbols(kb & query))
    result = tt_check_all(kb, query, symbols, {}, model_count)
    return result, model_count[0]


def tt_check_all(kb: 'Expr', query: 'Expr', symbols: list, model: dict, model_count: list):
    """Auxiliary routine to implement tt_entails."""
    if not symbols:
        # 'if' statement ensures that M(kb) is a subset of M(query)
        if pl_true(kb, model):
            result = pl_true(query, model)
            if result:
                model_count[0] += 1
            assert result in [True, False]
            return result
        else:
            return True
    else:
        p = symbols[0]
        rest = symbols[1:]
        return (tt_check_all(kb, query, rest, extend(model, p, True), model_count) and
                tt_check_all(kb, query, rest, extend(model, p, False), model_count))


def pl_true(exp: Union['Expr', bool], model: dict) -> Union[bool, None]:
    """Returns true if the expression is true in the given model."""
    if exp in [True, False]:
        return exp

    op = exp.op
    args = exp.args

    if is_symbol(op):
        return model.get(exp)
    elif op == '~':
        p = pl_true(args[0], model)
        return None if p is None else not p
    elif op == '||':
        result = False
        for arg in args:
            p = pl_true(arg, model)
            if p is True:
                return True
            elif p is None:
                result = None
        return result
    elif op == '&':
        result = True
        for arg in args:
            p = pl_true(arg, model)
            if p is False:
                return False
            if p is None:
                result = None
        return result

    p, q = args

    if op == '==>':
        return pl_true(~p | '||' | q, model)

    pt = pl_true(p, model)

    if pt is None:
        return None

    qt = pl_true(q, model)

    if op == '<=>':
        return pt == qt

    raise ValueError('Illegal operator in logic expression' + str(exp))


def pl_fc_entails(kb, q) -> bool:
    """
    [Figure 7.15]
    Use forward chaining to see if a PropDefiniteKB entails symbol q.
    > pl_fc_entails(horn_clauses_KB, expr('Q'))
    True
    """
    count = {c: len(conjuncts(c.args[0])) for c in kb.clauses if c.op == '==>'}
    inferred = defaultdict(bool)
    agenda = [s for s in kb.clauses if is_prop_symbol(s.op)]
    for item in agenda:
        fc_symbols.add(item)

    while agenda:
        p = agenda.pop()
        if p == q:
            return True
        if not inferred[p]:
            inferred[p] = True
            for c in kb.clauses_with_premise(p):
                count[c] -= 1
                fc_symbols.add(c.args[1])
                if count[c] == 0:
                    agenda.append(c.args[1])

    return False


def get_fc_symbols():
    return fc_symbols


def pl_bc_entails(kb, q) -> bool:
    inferred = defaultdict(bool)
    agenda = [q]
    prop_symbol = [s for s in kb.clauses if is_prop_symbol(s.op)]

    while agenda:
        p = agenda.pop()
        bc_symbols.append(p)
        if p in prop_symbol:
            return True
        if not kb.clauses_by_conclusion(p):
            return False
        if not inferred[p]:
            inferred[p] = True
            if not kb.clauses_by_conclusion(p):
                agenda.append(p)
            for c in kb.clauses_by_conclusion(p):
                if c.op == '==>':
                    bc_symbols.extend(conjuncts(c.args[0]))
                    agenda.extend(conjuncts(c.args[0]))
    return False


def get_bc_symbols():
    bc_symbols_set = set(bc_symbols)
    return bc_symbols_set
