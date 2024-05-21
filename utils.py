"""utils.py: Contains utility functions."""

from expr import Expr
from typing import Tuple


def file_parser(filename: str) -> Tuple[list, str]:
    file = open(filename, 'r')

    if file.closed:
        raise RuntimeError(f"file_parser: Failed to open file {filename}")

    file.readline()  # reads Tell
    kb_str = ""

    # get all the lines until "ASK" is reached
    while True:
        line = file.readline().strip()
        if "ask" in line.lower():
            break
        kb_str += line

    # convert the kb string into sentences
    kb = [x.strip() for x in kb_str.split(';') if x]
    query = file.readline().strip()  # get query

    return kb, query


def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)


def extend(s: dict, var: 'Expr', val: bool) -> dict:
    """Copy dict s and extend it by setting var to val; return copy."""
    return {**s, var: val}


def remove_all(value, array: list) -> list:
    """Removes all occurrences of 'value' from the given array."""
    return [x for x in array if x != value]
