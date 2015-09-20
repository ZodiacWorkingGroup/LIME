import re


def donothing(x):
    return x


class token:
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return 'Tok( "'+str(self.value)+'", '+str(self.tag)+' )'

    def __getitem__(self, s):
        return self.value[s]


class lexer:
    def __init__(self, base=[], basemethod=list.append, tokenclass=token):
        self.base = base
        self.tokens = []
        self.basemethod = basemethod
        self.tokenclass = tokenclass

    def add_token_expr(self, regex, tag, s=(0, None, 1), rewritefunction=donothing):
        self.tokens.append((regex, tag, slice(*s), rewritefunction))

    def lex(self, exp):
        r = self.base
        s = 0

        while s < len(exp):
            for x in self.tokens:
                match = re.match(x[0], exp[s:])
                if match:
                    if match.group(0):
                        if x[1]:
                            t = token(match.group(0), x[1])
                            t = t[x[2].start:x[2].stop:x[2].step]
                            if type(x[3]) == tuple:
                                if len(x[3]) > 1:
                                    t = x[3][0](t, *x[3][1:])
                                else:
                                    t = x[3][0](t)
                            else:
                                t = x[3](t)

                            self.basemethod(r, token(t, x[1]))
                        s += len(match.group(0))
                        break
                    else:
                        raise ValueError('Invalid character encountered: '+exp[s])
                continue
        return r
