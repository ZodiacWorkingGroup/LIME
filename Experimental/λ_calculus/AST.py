from copy import deepcopy


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
    def __init__(self, identity):
        self.id = identity

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


class IDAssignment(Assignment):
    def __init__(self, identity, exp):
        self.id = identity
        self.expression = exp

    def eval(self, env):
        env[self.id] = self.expression.eval(env)


# Removed Features
'''class Operator:
    def __init__(self, exp, lid, rid):
        self.exp = exp
        self.lid = lid
        self.rid = rid

    def eval(self, env, l, r):
        env2 = deepcopy(env)
        env2.update({self.lid: l, self.rid: r})
        return self.exp.eval(env2)


class OpExp(Expression):
    def __init__(self, l, r, op):
        self.l = l
        self.r = r
        self.op = op

    def eval(self, env):
        self.op.eval(env, self.l.eval(env), self.r.eval(env))


class OperatorAssignment(Assignment):
    def __init__(self, lid, rid, op, exp):
        self.lid = lid
        self.rid = rid
        self.op = op
        self.exp = exp

    def eval(self, env):
        env[self.op] = Operator(self.exp, self.lid, self.rid)'''
