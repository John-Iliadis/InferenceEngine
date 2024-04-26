from expr import Expr
from utils import is_symbol, associate, first


def to_cnf(s: 'Expr'):
    s = eliminate_implications(s)
    s = move_not_inwards(s)
    s = distribute_and_over_or(s)
    return s


def eliminate_implications(s: 'Expr') -> 'Expr':
    """Change implications into equivalent form with only &, |, and ~ as logical operators."""
    if not s.args or is_symbol(s.op):
        return s

    args = list(map(eliminate_implications, s.args))
    a, b = args[0], args[-1]

    if s.op == '==>':
        return ~a | '||' | b
    elif s.op == '<=>':
        return (~a | '||' | b) & (~b | '||' | a)
    else:
        assert s.op in ('&', '||', '~')
        return Expr(s.op, *args)


def move_not_inwards(s):
    """Rewrite sentence s by moving negation sign inward.
    move_not_inwards(~(A || B))
    (~A & ~B)
    """
    if s.op == '~':
        def NOT(b): return move_not_inwards(~b)

        a = s.args[0]
        if a.op == '~':
            return move_not_inwards(a.args[0])
        if a.op == '&':
            return associate('||', list(map(NOT, a.args)))
        if a.op == '||':
            return associate('&', list(map(NOT, a.args)))
        return s
    elif is_symbol(s.op) or not s.args:
        return s
    else:
        return Expr(s.op, *list(map(move_not_inwards, s.args)))


def distribute_and_over_or(s: 'Expr'):
    """Given a sentence s consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence in CNF.
    distribute_and_over_or((A & B) || C)
    ((A || C) & (B || C))
    """
    if s.op == '||':
        s = associate('||', s.args)
        if s.op != '||':
            return distribute_and_over_or(s)
        elif len(s.args) == 1:
            return distribute_and_over_or(s.args[0])
        elif len(s.args) == 0:
            assert False
            # return False  # todo: check why this returns false

        conj = first(arg for arg in s.args if arg.op == '&')

        if not conj:
            return s

        others = [a for a in s.args if a is not conj]
        rest = associate('||', others)

        return associate('&', [distribute_and_over_or(c | '||' | rest) for c in conj.args])
    elif s.op == '&':
        return associate('&', list(map(distribute_and_over_or, s.args)))
    else:
        return s
