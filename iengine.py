import sys
from inference_algorithms import tt_entails, fc_entails, bc_entails, dpll_entails, pl_resolution_entails
from expr import kb2expr, kb2expr_list, expr
from utils import file_parser


def main():
    if len(sys.argv) < 3:
        raise RuntimeError("Incorrect number of cmd args")

    filename = sys.argv[1]
    method_name = sys.argv[2].lower()

    kb, query = file_parser(filename)

    result_lhs, result_rhs = None, None

    if method_name == "tt":
        result_lhs, result_rhs = tt_entails(kb2expr(kb), expr(query))
    elif method_name == "fc":
        result_lhs, result_rhs = fc_entails(kb2expr_list(kb), expr(query))
    elif method_name == "bc":
        result_lhs, result_rhs = bc_entails(kb2expr_list(kb), expr(query))
    elif method_name == "dpll":
        result_lhs = dpll_entails(kb2expr(kb), expr(query))
        result_rhs = ''
    elif method_name == "pl":
        result_lhs = pl_resolution_entails(kb2expr(kb), expr(query))
        result_rhs = ''
    else:
        raise RuntimeError("Incorrect command line arguments")

    if result_lhs == True:
        print("Yes: " + (str(result_rhs) if not isinstance(result_rhs,
              list) else ", ".join([x.op for x in result_rhs])))
    else:
        print('No')


if __name__ == '__main__':
    main()
