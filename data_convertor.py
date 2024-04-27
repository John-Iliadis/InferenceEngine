import sys

file_name = sys.argv[1]
p = []
q = []


def data_convertor():
    line_count = 0
    with open(file_name, "r") as file:
        for line in file:
            line_count += 1
            if line_count == 2:
                tell = line.strip()
            if line_count == 4:
                q = line.strip()
                break
    p = [s.strip() for s in tell.split(';')]
    p = [s.rstrip() for s in p[:-1]]
    p = [s.replace('=>', '==>') for s in p]
    return file_name, p, q


data_convertor()
