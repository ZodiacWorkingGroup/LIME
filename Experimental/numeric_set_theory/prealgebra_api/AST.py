class Exp:
    def __repr__(self):
        return str(dir(self))


class NumExp(Exp):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return float(self.val)

    def __repr__(self):
        return '(NumExp: '+repr(self.val)+')'


class VarExp(Exp):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return float(env.get(self.name))

    def __repr__(self):
        return '(VarExp: '+repr(self.name)+')'


class OpExp(Exp):
    def __init__(self, l, r, op):
        self.left = l
        self.right = r
        self.op = op

    def eval(self, env):
        if self.op == '+':
            return self.left.eval(env)+self.right.eval(env)

        elif self.op == '-':
            return self.left.eval(env)-self.right.eval(env)

        elif self.op == '*':
            return self.left.eval(env)*self.right.eval(env)

        elif self.op == '/':
            return self.left.eval(env)/self.right.eval(env)

        elif self.op == '%':
            return self.left.eval(env)%self.right.eval(env)

        elif self.op == '^':
            return self.left.eval(env)**self.right.eval(env)

    def __repr__(self):
        return '(OpExp: '+repr(self.op)+', '+repr(self.left)+', '+repr(self.right)+')'


class ParenExp(Exp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        return self.exp.eval(env)

    def __repr__(self):
        return '(ParenExp: '+repr(self.exp)+')'
