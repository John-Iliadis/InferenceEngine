import sys
from inference_algorithms import tt_entails, fc_entails, bc_entails
from kb import PropDefiniteKB
from expr import expr, kb2expr
from utils import file_parser


def run_inference_algorithm(method_name: str, kb: list, query: str):
    query = expr(query)

    # if method_name.lower() == "tt":
    #     return tt_entails(kb2expr(kb), query)

    definite_clauses_kb = PropDefiniteKB(kb)

    if method_name.lower() == "fc":
        result, symbols = fc_entails(definite_clauses_kb, query)
        return result, symbols
    # elif method_name.lower() == "bc":
    #     result, symbols = pl_bc_entails(definite_clauses_kb, query)
    #     return result, symbols

    raise RuntimeError(f"select_inference_algorithm(): Invalid algorithm selected")


def main():
    if len(sys.argv) < 3:
        raise RuntimeError("Incorrect number of cmd args")

    filename = sys.argv[1]
    method_name = sys.argv[2]

    kb, query = file_parser(filename)

    result, symbols = run_inference_algorithm(method_name, kb, query)

    if result:
        symbol_str = ', '.join(str(symbol) for symbol in symbols)
        print("YES: " + symbol_str)
    else:
        print("NO")


if __name__ == '__main__':
    # main()
   # x: 'Expr' = expr('a&b&c==>d')

    kb, query = file_parser("data/problem_1.txt")
    definite_clauses_kb = PropDefiniteKB(kb)
    x, inferred = bc_entails(definite_clauses_kb, expr(query))
    print(x, inferred)
