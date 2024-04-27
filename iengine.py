import sys
from data_convertor import *
from entail_engine import *

file_name, p, q = data_convertor()
method = sys.argv[2]


def switch(method):  # to switch between different search algorithms
    if method.lower() == "tt":
        return tt_entails(p, q)
    # elif method.lower() == "fc":
    #     return
    # elif method.lower() == "bc":
    #     return
    else:
        print("Invalid method")


def main():
    result = switch(method)
    if len(sys.argv) < 3:
        print("Please Enter Correct Argument")
    if result is not None:
        print(result)


main()
