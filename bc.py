from collections import defaultdict
from cnf import *
from expr import *

symbols = []
symbol_list = set()


def pl_bc_entails(kb, q):
    """
    [Figure 7.15]
    Use forward chaining to see if a PropDefiniteKB entails symbol q.
    >>> pl_fc_entails(horn_clauses_KB, expr('Q'))
    True
    """
    count = {c: len(conjuncts(c.args[0])) for c in kb.clauses if c.op == '==>'}
    # rhs = {c: conjuncts(c.args[1]) for c in kb.clauses if c.op == '==>'}
    inferred = defaultdict(bool)
    agenda = [q]
    prop_symbol = [s for s in kb.clauses if is_prop_symbol(s.op)]
    for c in kb.clauses:
        if c.op == '==>':
            for c1 in conjuncts(c.args[0]):
                symbol_list.add(c1)
            for c2 in conjuncts(c.args[0]):
                symbol_list.add(c2)

    while agenda:
        p = agenda.pop()
        # if p in prop_symbol:
        if p in prop_symbol:
            return True
        if not inferred[p]:
            inferred[p] = True
            symbols.append(p)
            for c in kb.clauses_by_conclusion(p):
                print(kb.clauses_by_conclusion(p))
                if c.op == '==>':
                    for c2 in conjuncts(c.args[0]):
                        agenda.append(c2)
                        print("agenda: ")
                        print(agenda)

    return False


def get_bc_symbols():
    return symbols
