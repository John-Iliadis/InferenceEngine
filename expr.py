"""expr.py: This file contains all classes and functions associated with expressions."""

import collections
from typing import List


class Expr:
    def __init__(self, op: str, *args):
        self.op = op
        self.args = args

    def __invert__(self):
        return Expr('~', self)

    def __and__(self, rhs):
        return Expr('&', self, rhs)

    def __or__(self, rhs: str):
        return PartialExpr(rhs, self)

    def __rand__(self, lhs):
        return Expr('&', lhs, self)

    def __eq__(self, other):
        return isinstance(other, Expr) and self.op == other.op and self.args == other.args

    def __lt__(self, other):
        return isinstance(other, Expr) and str(self) < str(other)

    def __hash__(self):
        return hash(self.op) ^ hash(self.args)

    def __repr__(self):
        op = self.op
        args = [str(arg) for arg in self.args]
        if op.isidentifier():
            return f"{op}({', '.join(args)})" if args else op
        elif len(args) == 1:
            return op + args[0]
        else:
            opp = f" {op} "
            return f"({opp.join(args)})"


class PartialExpr:
    def __init__(self, op: str, lhs):
        self.op = op
        self.lhs = lhs

    def __or__(self, rhs):
        return Expr(self.op, self.lhs, rhs)

    def __repr__(self):
        return f"PartialExpr('{self.op}', '{self.lhs}')"


def Symbol(name) -> 'Expr':
    return Expr(name)


class DefaultKeyDict(collections.defaultdict):
    def __missing__(self, key):
        self[key] = result = self.default_factory(key)
        return result


def handle_infix_ops(x: str) -> str:
    for op in ['||', '<=>', '==>',]:
        x = x.replace(op, f"| '{op}' |")
    return x


def expr(x: str):
    assert x, 'x is empty'
    formatted_expr = handle_infix_ops(x)
    return eval(formatted_expr, DefaultKeyDict(Symbol))


def kb2expr(kb: List[str]) -> 'Expr':
    """
    Turns a kb into an expression.
    > kb2expr(['magical', 'mythical'])
    (magical & mythical)
    """
    kb_expr: str = ''

    for sentence in kb:
        sentence = sentence.replace('=>', '==>')
        kb_expr += f'&({sentence})' if kb_expr else f'({sentence})'

    return expr(kb_expr)


def associate(op, args):
    """Given an associative op, return an expression with the same
    meaning as Expr(op, *args), but flattened -- that is, with nested
    instances of the same op promoted to the top level.
    > associate('&', [(A&B),(B|C),(B&C)])
    (A & B & (B | C) & B & C)
    > associate('|', [A|(B|(C|(A&B)))])
    (A | B | C | (A & B))
    """
    _op_identity = {'&': True, '||': False}

    args = dissociate(op, args)

    if len(args) == 0:
        assert False
        # return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return Expr(op, *args)


def dissociate(op, args) -> list:
    """Returns all the terms that are connected with 'op'.
    > dissociate('&', [A & B & (C || D)])
    [A, B, (C || D)]
    """
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.op == op:
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result


def is_symbol(s: str) -> bool:
    """Returns true if the first character of s is a letter."""
    return s[:1].isalpha()


def get_symbols(x: 'Expr') -> set:
    """Returns all propositional symbols in x."""
    if is_symbol(x.op):
        return {x}
    else:
        return {symbol for arg in x.args for symbol in get_symbols(arg)}
