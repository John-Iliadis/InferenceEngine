import sys
from inference_algorithms import tt_entails, fc_entails, bc_entails, dpll_entails
from expr import kb2expr, kb2expr_list, expr
from utils import file_parser


def main():
    if len(sys.argv) < 3:
        raise RuntimeError("Incorrect number of cmd args")

    filename = sys.argv[1]
    method_name = sys.argv[2].lower()

    kb, query = file_parser(filename)

    result_lhs, result_rhs = None, None

    if method_name not in ["tt", "fc", "bc", "dpll"]:
        raise ValueError("Incorrect algorithm name. Should be one of [tt, fc, bc, dpll]")

    if method_name == "tt":
        result_lhs, result_rhs = tt_entails(kb2expr(kb), expr(query))
    elif method_name == "fc":
        result_lhs, result_rhs = fc_entails(kb2expr_list(kb), expr(query))
    elif method_name == "bc":
        result_lhs, result_rhs = bc_entails(kb2expr_list(kb), expr(query))
    elif method_name == "dpll":
        result_lhs, result_rhs = dpll_entails(kb2expr(kb), expr(query))

    if method_name in ["tt", "fc", "bc"]:
        if result_lhs == True:
            print("Yes: " + (str(result_rhs) if not isinstance(result_rhs, list) else ", ".join([x.op for x in result_rhs])))
        else:
            print('No')
    elif method_name == "dpll":
        if result_lhs == True:
            print("Yes")
        else:
            print(f"No: {result_rhs}")


if __name__ == '__main__':
    main()
