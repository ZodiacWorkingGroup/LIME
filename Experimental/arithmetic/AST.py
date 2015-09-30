class Exp:
    def __repr__(self):
        return str(dir(self))


class NumExp(Exp):
    def __init__(self, val):
        self.val = val

    def eval(self):
        return float(self.val)

    def __repr__(self):
        return '(NumExp: '+repr(self.val)+')'


class OpExp(Exp):
    def __init__(self, l, r, op):
        self.left = l
        self.right = r
        self.op = op

    def eval(self):
        if self.op == '+':
            return self.left.eval()+self.right.eval()

        elif self.op == '-':
            return self.left.eval()-self.right.eval()

        elif self.op == '*':
            return self.left.eval()*self.right.eval()

        elif self.op == '/':
            return self.left.eval()/self.right.eval()

        elif self.op == '%':
            return self.left.eval()%self.right.eval()

        elif self.op == '^':
            return self.left.eval()**self.right.eval()

    def __repr__(self):
        return '(OpExp: '+repr(self.op)+', '+repr(self.left)+', '+repr(self.right)+')'


class ParenExp(Exp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self):
        return self.exp.eval()

    def __repr__(self):
        return '(ParenExp: '+repr(self.exp)