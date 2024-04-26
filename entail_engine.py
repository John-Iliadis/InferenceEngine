"""entail_engine.py: File containing entailment algorithms."""

from expr import Expr, is_symbol, get_symbols
from utils import extend
from typing import Union


def tt_entails(kb: 'Expr', query: 'Expr') -> bool:
    """A truth table enumeration algorithm for deciding propositional entailment."""
    symbols = list(get_symbols(kb & query))
    return tt_check_all(kb, query, symbols, {})


def tt_check_all(kb: 'Expr', query: 'Expr', symbols: list, model: dict) -> bool:
    """Auxiliary routine to implement tt_entails."""
    if not symbols:
        if pl_true(kb, model):
            result = pl_true(query, model)
            assert result in [True, False]
            return result
        else:
            return True
    else:
        p = symbols[0]
        rest = symbols[1:]
        return (tt_check_all(kb, query, rest, extend(model, p, True)) and
                tt_check_all(kb, query, rest, extend(model, p, False)))


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
