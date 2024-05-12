"""inference_algorithms.py: File containing entailment algorithms."""

from expr import Expr, is_symbol, get_symbols, conjuncts, disjuncts, clauses_with_premise, clauses_with_conclusion, is_definite_clause, expr
from utils import extend, remove_all
from typing import Tuple, Union, List
from collections import defaultdict, deque
from cnf import to_cnf


# ______________________________________________________________________________
# TT-Entails

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
            return result if result is not None else False
        return True
    else:
        p = symbols[0]
        rest = symbols[1:]
        return (tt_check_all(kb, query, rest, extend(model, p, True), model_count) and
                tt_check_all(kb, query, rest, extend(model, p, False), model_count))


def pl_true(exp: 'Expr', model: dict) -> Union[bool, None]:
    """Returns true if the expression is true in the given model."""
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
            elif p is None:
                result = None
        return result

    p, q = args

    if op == '=>':
        return pl_true(~p | '||' | q, model)

    pt = pl_true(p, model)

    if pt is None:
        return None

    qt = pl_true(q, model)

    if qt is None:
        return None

    if op == '<=>':
        return pt == qt

    raise ValueError('Illegal operator in logic expression' + str(exp))


# ______________________________________________________________________________
# FC-Entails

def fc_entails(kb: List['Expr'], query: 'Expr') -> Tuple[bool, list]:
    assert all(is_definite_clause(e) for e in kb), "fc_entails: an expression in the kb is not in definite form"
    count = {c: len(conjuncts(c.args[0])) for c in kb if c.op == '=>'}
    inferred = defaultdict(bool)
    agenda = deque([s for s in kb if is_symbol(s.op)])
    inferred_symbols = []

    while agenda:
        proposition = agenda.popleft()

        if proposition == query:
            inferred_symbols.append(proposition)
            return True, inferred_symbols
        if not inferred[proposition]:
            inferred[proposition] = True
            inferred_symbols.append(proposition)
            for clause in clauses_with_premise(kb, proposition):
                count[clause] -= 1
                if count[clause] == 0:
                    agenda.append(clause.args[1])

    return False, inferred_symbols


# ______________________________________________________________________________
# BC-Entails

def bc_entails(kb: List['Expr'], query: 'Expr') -> Tuple[bool, list]:
    assert all(is_definite_clause(e) for e in kb), "bc_entails: an expression in the kb is not in definite form"
    symbols = [s for s in kb if is_symbol(s.op)]
    inferred_symbols = []  # list of symbols that are entailed by bc
    expr_cache = []  # cache that stores calculated definite clauses, so they don't have to be re-calculated

    # recursive impl of bc
    def truth_value(q) -> bool:
        if q in symbols:
            inferred_symbols.append(q) if q not in inferred_symbols else 0  # store symbol if it's not already entailed
            return True
        elif not is_symbol(q.op):
            return truth_value(q.args[0]) and truth_value(q.args[1])
        else:
            for clause in clauses_with_conclusion(kb, q):
                if clause in expr_cache:
                    return True  # clause is already in the cache, so return True
                elif truth_value(clause.args[0]):
                    expr_cache.append(clause)  # add evaluated expr to the cache
                    inferred_symbols.append(clause.args[1])  # add new inferred symbol
                    return True
            return False

    return truth_value(query), inferred_symbols


# ______________________________________________________________________________
# DPLL-Entails

def dpll_entails(kb: 'Expr', query: 'Expr') -> bool:
    _sentence = kb & ~query  # kb |= query if (kb & ~query) is unsatisfiable
    _symbols = list(get_symbols(_sentence))
    clauses = conjuncts(to_cnf(_sentence))

    def dpll_impl(symbols: list, model: dict):
        unknown_clauses = []

        for clause in clauses:
            result = pl_true(clause, model)
            if result is False:
                return False
            elif result is None:
                unknown_clauses.append(clause)

        if not unknown_clauses:
            return True

        p, value = find_pure_symbol(symbols, unknown_clauses)

        if p is not None:
            return dpll_impl(remove_all(p, symbols), extend(model, p, value))

        p, value = find_unit_clause(clauses, model)

        if p is not None:
            return dpll_impl(remove_all(p, symbols), extend(model, p, value))

        p = symbols[0]
        rest = symbols[1:]

        return dpll_impl(rest, extend(model, p, True)) or dpll_impl(rest, extend(model, p, False))

    return not dpll_impl(_symbols, {})  # if all models are false, then the query is entailed by kb


def find_pure_symbol(symbols: list, clauses: list):
    for symbol in symbols:
        found_pos, found_neg = False, False
        for clause in clauses:
            disjuncts_list = disjuncts(clause)
            if not found_pos and symbol in disjuncts_list:
                found_pos = True  # found a clause where the symbol is true
            if not found_neg and ~symbol in disjuncts_list:
                found_neg = True  # found a clause where the symbol is false
        if found_pos != found_neg:  # if the symbol is true/false in all clauses, then return it
            return symbol, found_pos
    return None, None


def find_unit_clause(clauses: list, model: dict):
    for clause in clauses:
        p, value = unit_clause_assign(clause, model)
        if p is not None:
            return p, value
    return None, None


def unit_clause_assign(clause: 'Expr', model: dict):
    p, value = None, None

    for literal in disjuncts(clause):
        symbol, is_positive = inspect_literal(literal)
        if symbol in model:
            if model[symbol] == is_positive:
                return None, None  # clause already true
        elif p is not None:
            return None, None  # more than 1 unbound variable
        else:
            p, value = symbol, is_positive
    return p, value


def inspect_literal(literal: 'Expr') -> Tuple['Expr', bool]:
    """Returns the symbol of the literal and the value that makes the literal true."""
    if literal.op == '~':
        return literal.args[0], False
    return literal, True
