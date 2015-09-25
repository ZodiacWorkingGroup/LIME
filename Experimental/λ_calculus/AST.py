class Name:
    def __init__(self, name):
        self.name = name


class Function:
    def __init__(self, name, exp):
        self.name = name
        self.expression = exp


class Application:
    def __init__(self, l, r):
        self.left = l
        self.right = r