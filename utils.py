"""utils.py: Contains utility functions."""

from expr import Expr, expr
from typing import Tuple


def file_parser(filename: str) -> Tuple[list, 'Expr']:
    file = open(filename, 'r')

    if file.closed:
        raise RuntimeError(f"file_parser: Failed to open file {filename}")

    file.readline()  # reads Tell
    kb_str = file.readline().strip()  # get kb string
    kb = convert_kb_to_list(kb_str)  # convert kb string to a list
    get_next_non_blank_line(file)  # remove any blank lines and get to ASK
    query = file.readline().strip()  # get query

    return kb, expr(query)


def convert_kb_to_list(kb_str: str) -> list:
    """Converts a kb string to a list of sentences."""
    kb = []

    for sentence in kb_str.split(';'):
        if sentence:
            sentence = sentence.replace('=>', '==>').strip()
            kb.append(sentence)

    return kb


def get_next_non_blank_line(file):
    """Discards all the blank lines until it gets to a non-blank line."""
    line = file.readline().strip()

    while line == "":
        line = file.readline().strip()

    return line


def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)


def extend(s: dict, var: 'Expr', val: bool) -> dict:
    """Copy dict s and extend it by setting var to val; return copy."""
    return {**s, var: val}


def remove_all(value, array: list) -> list:
    """Removes all occurrences of 'value' from the given array."""
    return [x for x in array if x != value]
