class Exp:
    pass


class NumExp(Exp):
    def __init__(self, val):
        self.val = val

    def eval(self):
        return float(self.val)


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


class ParenExp(Exp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self):
        return self.exp.eval()