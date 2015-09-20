from copy import deepcopy


class Result:
    def __init__(self, value, env):
        self.value = value
        self.env = env


class Equality:
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Exp(Equality):
    def eval(self, env):  # Overloaded in subclasses
        return None


class NumExp(Exp):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return Result(float(self.value), env)


class VarExp(Exp):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        if self.name in env:
            return Result(env['variables'][self.name], env)
        else:
            return None


class ParenExp(Exp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        return self.exp.eval(env)


class BinExp(Exp):
    def __init__(self, op, l, r):
        self.op = op
        self.lhs = l
        self.rhs = r

    def eval(self, env):
        if self.op == '+':
            return Result(self.lhs.eval(env).value + self.rhs.eval(env).value, env)
        elif self.op == '-':
            return Result(self.lhs.eval(env).value - self.rhs.eval(env).value, env)
        elif self.op == '*':
            return Result(self.lhs.eval(env).value * self.rhs.eval(env).value, env)
        elif self.op == '/':
            return Result(self.lhs.eval(env).value / self.rhs.eval(env).value, env)
        elif self.op == '%':
            return Result(self.lhs.eval(env).value % self.rhs.eval(env).value, env)
        elif self.op == '**':
            return Result(self.lhs.eval(env).value ** self.rhs.eval(env).value, env)
        elif self.op in ['&', '|', '^', '>>', '<<']:
            if self.op == '&':
                return Result(self.lhs.eval(env).value & self.rhs.eval(env).value, env)
            elif self.op == '|':
                return Result(self.lhs.eval(env).value | self.rhs.eval(env).value, env)
            elif self.op == '^':
                return Result(self.lhs.eval(env).value ^ self.rhs.eval(env).value, env)
            elif self.op == '>>':
                return Result(self.lhs.eval(env).value >> self.rhs.eval(env).value, env)
            elif self.op == '<<':
                return Result(self.lhs.eval(env).value << self.rhs.eval(env).value, env)
        elif self.op in env['operators']:
            pass
        else:
            return None


class UnExp(Exp):
    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    def eval(self, env):
        if self.op == '~':
            return Result(~self.arg.eval(env).value, env)
        else:
            return None


class FuncExp(Exp):
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def eval(self, env):
        if self.name in env['builtin-functions']:  # Built-in functions
            return Result(env['builtin-functions'](*self.args).value, env)
        elif self.name in env['functions']:  # User-defined functions
            func = env['functions'][self.name]
            funcenv = deepcopy(env)  # Make a copy of the environment that will be updated and passed to the function

            for x in range(len(func['argnames'])):  # Give funcenv its arguments
                funcenv.update({func['argnames'][x]: self.args[x]})

            return Result(func['exp'].eval(funcenv), env)  # Return evaluation with the pre-function environment
        else:
            return None
