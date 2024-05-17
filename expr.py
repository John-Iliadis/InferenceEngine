"""expr.py: This file contains all classes and functions associated with expressions."""

import collections
import re
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
    x = re.sub(r'(?<!<)=>', "| '=>' |", x)
    x = x.replace('<=>', "| '<=>' |")
    x = x.replace('||', "| '||' |")
    return x


def expr(x: str):
    assert x, 'x is empty'
    formatted_expr = handle_infix_ops(x)
    return eval(formatted_expr, DefaultKeyDict(Symbol))


def kb2expr(kb: List[str]) -> 'Expr':
    """
    Turns a string list kb into an expression.
    > kb2expr(['magical', 'mythical'])
    (magical & mythical)
    """
    kb_expr: str = ''

    for sentence in kb:
        kb_expr += f'&({sentence})' if kb_expr else f'({sentence})'

    return expr(kb_expr)


def kb2expr_list(kb: List[str]) -> List['Expr']:
    """Turns a string list kb into an Expr list."""
    return [expr(e) for e in kb]


def associate(op: str, args):
    """Given an associative op, return an expression with the same
    meaning as Expr(op, *args), but flattened -- that is, with nested
    instances of the same op promoted to the top level.
    > associate('&', [(A&B),(B|C),(B&C)])
    (A & B & (B | C) & B & C)
    > associate('|', [A|(B|(C|(A&B)))])
    (A | B | C | (A & B))
    """
    args = dissociate(op, args)

    if len(args) == 0:
        assert False
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


def conjuncts(s: 'Expr') -> list:
    """Return a list of the conjuncts in the sentence s.
    > conjuncts(A & B & C)
    [A, B, C]
    > conjuncts(A | B)
    [(A | B)]
    """
    return dissociate('&', [s])


def disjuncts(s: 'Expr') -> list:
    """Return a list of the disjuncts in the sentence s.
    > disjuncts(A | B)
    [A, B]
    > disjuncts(A & B)
    [(A & B)]
    """
    return dissociate('||', [s])


def is_definite_clause(s: 'Expr'):
    """Returns True for expr s of the form A & B & ... & C => D,
    where all literals are positive. In clause form, this is
    ~A | ~B | ... | ~C | D, where exactly one clause is positive.
    > is_definite_clause(expr('Farmer(Mac)'))
    True
    """
    if is_symbol(s.op):
        return True
    elif s.op == '=>':
        antecedent, consequent = s.args
        return is_symbol(consequent.op) and all(is_symbol(arg.op) for arg in conjuncts(antecedent))
    else:
        return False


def is_symbol(s: str) -> bool:
    """Returns true if the first character of s is a letter."""
    return s[:1].isalpha()


def get_symbols(x: 'Expr') -> set:
    """Returns all propositional symbols in x."""
    if is_symbol(x.op):
        return {x}
    else:
        return {symbol for arg in x.args for symbol in get_symbols(arg)}


def clauses_with_premise(clauses, p):
    """Return a list of the clauses in KB that have p in their premise."""
    return [c for c in clauses if c.op == '=>' and p in conjuncts(c.args[0])]


def clauses_with_conclusion(clauses, p):
    """Return a list of the clauses in KB that have p in their conclusion."""
    return [c for c in clauses if c.op == '=>' and p in conjuncts(c.args[1])]
