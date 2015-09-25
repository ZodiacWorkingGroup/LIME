#!~/anaconda/bin/python
# -*- coding: utf-8 -*-
from UtopiaLexer import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support (for λ character)

# Tags
LAMBDA = 'LAMBDA'
PAREN = 'PAREN'
DOT = 'DOT'
EQ = 'EQ'
ID = 'ID'
NAME = 'NAME'


def lexl(exp):  # Lex a single line
    def lam(s):
        return 'LAMBDA'

    lexr = lexer()  # Create a Lexer object

    lexr.add_token_expr(r'#.*', None)  # Comments
    lexr.add_token_expr(r'^[\s]', None)  # Ignore whitespace (never newlines, as those are split by in lex())
    lexr.add_token_expr(u'^λ', LAMBDA, (0, None, 1), lam)  # λ keyword
    lexr.add_token_expr(r'^[()]', PAREN)  # Parentheses
    lexr.add_token_expr(r'^\.', DOT)  # . keyword
    lexr.add_token_expr(r'^=', EQ)  # Equal sign
    lexr.add_token_expr(r'^[a-z]', NAME)  # variables/names in λ-expressions
    lexr.add_token_expr(r'^.', ID)  # IDs that can have λ-expressions assigned to them

    return lexr.lex(exp)


def lex(lines):
    return [lexl(x) for x in lines.strip('\n').split('\n')]  # split by newlines and lex lines and return list of result

if __name__ == '__main__':
    print(lex('$ = λx.y\n(λx.x)$'))  # λx.x is an expression (the identity function) and $ is a named expression
    input()
