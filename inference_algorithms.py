"""inference_algorithms.py: File containing entailment algorithms."""

from expr import Expr, is_symbol, get_symbols
from utils import extend
from typing import Tuple
from collections import defaultdict, deque
from cnf import conjuncts


def tt_entails(kb: 'Expr', query: 'Expr') -> Tuple[bool, int]:
    """A truth table enumeration algorithm for deciding propositional entailment."""
    model_count = [0]  # single element array so I can pass it as a reference
    symbols = list(get_symbols(kb & query))
    result = tt_check_all(kb, query, symbols, {}, model_count)
    return result, model_count[0]


def tt_check_all(kb: 'Expr', query: 'Expr', symbols: list, model: dict, model_count: list) -> bool:
    """Auxiliary routine to implement tt_entails."""
    if not symbols:
        # 'if' statement ensures that M(kb) is a subset of M(query)
        if pl_true(kb, model):
            result = pl_true(query, model)
            model_count[0] += 1 if result else 0
            return result
        return True
    else:
        p = symbols[0]
        rest = symbols[1:]
        return (tt_check_all(kb, query, rest, extend(model, p, True), model_count) and
                tt_check_all(kb, query, rest, extend(model, p, False), model_count))


def pl_true(exp: 'Expr', model: dict) -> bool:
    """Returns true if the expression is true in the given model."""
    op = exp.op
    args = exp.args

    if is_symbol(op):
        return model.get(exp, False)
    elif op == '~':
        return not pl_true(args[0], model)
    elif op == '||':
        for arg in args:
            if pl_true(arg, model):
                return True
        return False
    elif op == '&':
        for arg in args:
            if pl_true(arg, model) is False:
                return False
        return True

    p, q = args

    if op == '==>':
        return pl_true(~p | '||' | q, model)
    elif op == '<=>':
        return pl_true(p, model) == pl_true(q, model)

    raise ValueError('Illegal operator in logic expression' + str(exp))


def pl_fc_entails(kb, query) -> Tuple[bool, list]:
    """
    [Figure 7.15]
    Use forward chaining to see if a PropDefiniteKB entails symbol q.
    > pl_fc_entails(horn_clauses_KB, expr('Q'))
    True
    """
    count = {c: len(conjuncts(c.args[0])) for c in kb.clauses if c.op == '==>'}
    inferred = defaultdict(bool)
    agenda = deque([s for s in kb.clauses if is_symbol(s.op)])
    entailed_symbols = []

    while agenda:
        proposition = agenda.popleft()

        if proposition == query:
            entailed_symbols.append(proposition)
            return True, entailed_symbols
        if not inferred[proposition]:
            inferred[proposition] = True
            entailed_symbols.append(proposition)
            for clause in kb.clauses_with_premise(proposition):
                count[clause] -= 1
                if count[clause] == 0:
                    agenda.append(clause.args[1])

    return False, entailed_symbols


def pl_bc_entails(kb, query) -> Tuple[bool, list]:
    inferred = defaultdict(bool)
    agenda = [query]
    prop_symbol = [s for s in kb.clauses if is_symbol(s.op)]
    entailed_symbols = []

    while agenda:
        p = agenda.pop()
        entailed_symbols.append(p)
        if p in prop_symbol:
            return True, entailed_symbols
        if not kb.clauses_by_conclusion(p):
            return False, entailed_symbols
        if not inferred[p]:
            inferred[p] = True
            if not kb.clauses_by_conclusion(p):
                agenda.append(p)
            for c in kb.clauses_by_conclusion(p):
                if c.op == '==>':
                    entailed_symbols.extend(conjuncts(c.args[0]))
                    agenda.extend(conjuncts(c.args[0]))
