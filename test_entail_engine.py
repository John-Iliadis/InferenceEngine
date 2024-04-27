"""test_entail_engine.py: Tests entailment algorithms."""

from entail_engine import pl_true, tt_entails
from expr import Expr, expr


def test_pl_true():
    expr1 = expr('a || b')
    model_1 = {Expr('a'): False, Expr('b'): True}

    expr2 = expr('(magical & horned) ==> mythical')
    model_2 = {Expr('magical'): True, Expr('mythical')
                    : False, Expr('horned'): True}

    expr3 = expr(
        '((smoke & heat) ==> fire) <=> ((smoke ==> fire) || (heat ==> fire))')
    model_3 = {Expr('smoke'): False, Expr('heat'): False, Expr('fire'): False}

    assert pl_true(expr1, model_1) is True
    assert pl_true(expr2, model_2) is False
    assert pl_true(expr3, model_3) is True


def test_tt_entails():
    kb1 = expr('A & (B || C) & D & E & ~(F || G)')
    query_1 = expr('A & D & E & ~F & ~G')

    kb2 = expr('P || Q')
    query_2 = expr('Q')

    kb3 = expr('P & Q')
    query_3 = expr('Q')

    assert tt_entails(kb1, query_1) is True
    assert tt_entails(kb2, query_2) is False
    assert tt_entails(kb3, query_3) is True
