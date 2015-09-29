from UtopiaLexer import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support

# Tags
NUM = 'NUMBER'
OP = 'OP'
PAREN = 'PAREN'


def lexl(exp):  # Lex a single line
    lexr = lexer()  # Create a Lexer object

    lexr.add_token_expr('^[0-9]+(\.[0-9]+)?', NUM)
    lexr.add_token_expr('^(\+|-|/|\*|%|^)', OP)
    lexr.add_token_expr('^[()]', PAREN)

    return lexr.lex(exp)