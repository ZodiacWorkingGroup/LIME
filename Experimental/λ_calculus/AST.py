from copy import deepcopy


class Expression:
    pass


class Assignment:
    pass


class Operator:
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env, l, r):
        env2 = deepcopy(env)
        # Add l and r to env2
        return self.exp.eval(env2)


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

    def eval(self, env):
        self.op.eval(env, self.l.eval(env), self.r.eval(env))


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

    def eval(self, env):
        env[self.op] = Operator(self.exp)
