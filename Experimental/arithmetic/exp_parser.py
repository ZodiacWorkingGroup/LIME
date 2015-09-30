# This parser is stolen almost in its entirety from Jay Conrod.

# I still don't want you to sue me.

from AST import *
from parser_combinators import *
from lexer import *
from functools import reduce


def keyword(kw, tag):
    return Reserved(kw, tag)

num = Tag(NUM) ^ (lambda i: float(i))


def aexp_value():
    return num ^ (lambda i: NumExp(i))


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def aexp_group():
    return keyword('(', PAREN) + Lazy(parsetoks) + keyword(')', PAREN) ^ process_group


def aexp_term():
    return aexp_value() | aexp_group()


def process_binop(op):
    return lambda l, r: OpExp(l, r, op)


def any_operator_in_list(ops):
    op_parsers = [keyword(op[0], OP) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

aexp_precedence_levels = [
    [('^', 'r')],
    [('*', 'l'), ('/', 'l'), ('%', 'l')],
    [('+', 'l'), ('-', 'l')],
]


def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        if precedence_level[1] == 'l':
            parser = parser * op_parser(precedence_level[0])
        elif precedence_level[1] == 'r':
            parser = op_parser(precedence_level[0]) * parser
    return parser


def parsetoks():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)


def parser():
    return Phrase(parsetoks())


def parse_tokens(tokens):
    ast = parser()(tokens, 0)
    return ast


def parse(script):
    return parse_tokens(lex(script))

if __name__ == '__main__':
    print(parse(input()))