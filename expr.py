import collections


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
        """x == y' evaluates to True or False; does not build an Expr."""
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


def Symbol(name):
    return Expr(name)


class DefaultKeyDict(collections.defaultdict):
    def __missing__(self, key):
        self[key] = result = self.default_factory(key)
        return result


def handle_infix_ops(x: str) -> str:
    for op in ['||', '=>', '<=>']:
        x = x.replace(op, f"| '{op}' |")
    return x


def expr(x: str) -> 'Expr':
    formatted_expr = handle_infix_ops(x)
    return eval(formatted_expr, DefaultKeyDict())
