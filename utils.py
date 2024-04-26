"""utils.py: Contains utility functions."""

from expr import Expr


def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)


def extend(s: dict, var: 'Expr', val: bool) -> dict:
    """Copy dict s and extend it by setting var to val; return copy."""
    return {**s, var: val}
