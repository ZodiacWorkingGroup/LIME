from exp_parser import *


def evalexp(exp):
    return parse(exp).eval()

while __name__ == '__main__':
    print(evalexp(input()))