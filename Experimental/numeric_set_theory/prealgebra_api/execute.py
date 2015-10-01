from exp_parser import *


def evalexp(exp, env):
    return parse(exp).eval(env)

while __name__ == '__main__':
    env = {}
    i = None
    while i != '':
        k = input('Key: ')
        i = input('Value: ')
        if k and i:
            env[k] = i

    print(evalexp(input(), env))
    print()
