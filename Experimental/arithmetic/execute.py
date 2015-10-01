from exp_parser import *


def evalexp(exp):
    return parse(exp).eval(env)

while __name__ == '__main__':
    print(evalexp(input()))
