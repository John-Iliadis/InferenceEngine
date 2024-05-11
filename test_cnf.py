"""test_cnf.py: Tests cnf.py"""

from cnf import eliminate_implications, move_not_inwards, distribute_and_over_or, to_cnf
from expr import Expr, expr, Symbol, associate, dissociate


def test_dissociate():
    expr1 = expr('a & b')
    expr2 = expr('(a & b) & (c || b) & d')
    expr3 = expr('(a <=> b) || (c => a) || c || d')

    assert dissociate('&', expr1.args) == list(expr('a, b'))
    assert dissociate('&', expr2.args) == list(expr('a, b, c || b, d'))
    assert dissociate('||', expr3.args) == list(expr('a <=> b, c => a, c, d'))


def test_associate():
    expr1 = expr('(a & b) & (b || c) & (b & c)')
    expr2 = expr('a || (b || (c || (a & b)))')

    x = associate('||', expr2.args)
    assert associate('&', expr1.args) == Expr('&', Symbol('a'), Symbol('b'), expr('(b || c)'), Symbol('b'), Symbol('c'))
    assert associate('||', expr2.args) == Expr('||', Symbol('a'), Symbol('b'), Symbol('c'), expr('a & b'))


def test_eliminate_implications():
    expr1 = expr('a <=> b')
    expr2 = expr('a => b')
    expr3 = expr('((~a & b) || c) => d')

    assert eliminate_implications(expr1) == expr('(~a || b) & (~b || a)')
    assert eliminate_implications(expr2) == expr('~a || b')
    assert eliminate_implications(expr3) == expr('~((~a & b) || c) || d')


def test_move_not_inwards():
    expr1 = expr('~(~a)')
    expr2 = expr('~(a & b)')
    expr3 = expr('~(a || b)')

    assert move_not_inwards(expr1) == expr('a')
    assert move_not_inwards(expr2) == expr('~a || ~b')
    assert move_not_inwards(expr3) == expr('~a & ~ b')


def test_distribute_and_over_or():
    expr1 = expr('(a & b) || c')
    expr2 = expr('((a => (b & c)) & d) || (b <=> d)')

    assert distribute_and_over_or(expr1) == expr('(a || c) & (b || c)')
    assert distribute_and_over_or(expr2) == expr('((a => (b & c)) || (b <=> d)) & (d || (b <=> d))')


def test_to_conjunctive_normal_form():
    expr1 = expr('~(b || c)')
    expr2 = expr('a || (b & c)')

    assert to_cnf(expr1) == expr('~b & ~c')
    assert to_cnf(expr2) == expr('(b || a) & (c || a)')  # distributivity of || over &
