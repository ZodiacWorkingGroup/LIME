class Expression:
    pass


class Assignment:
    pass


class Name(Expression):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        pass


class ID(Expression):
    def __init__(self, id):
        self.id = id

    def eval(self, env):
        if self.id in env:
            return env[self.id]
        else:
            raise ValueError('Invalid ID: '+self.id)


class Function(Expression):
    def __init__(self, name, exp):
        self.name = name
        self.expression = exp

    def eval(self, env):
        pass


class Application(Expression):
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def eval(self, env):
        pass


class OpExp(Expression):
    def __init__(self, l, r, op):
        self.l = l
        self.r = r
        self.op = op


class IDAssignment(Assignment):
    def __init__(self, id, exp):
        self.id = id
        self.expression = exp

    def eval(self, env):
        env[self.id] = self.expression.eval(env)


class OperatorAssignment(Assignment):
    def __init__(self, lid, rid, op, exp):
        self.lid = lid
        self.rid = rid
        self.op = op
        self.exp = exp