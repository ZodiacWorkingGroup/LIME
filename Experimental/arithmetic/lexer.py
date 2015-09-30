from UtopiaLexer import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support

# Tags
NUM = 'NUMBER'
OP = 'OP'
PAREN = 'PAREN'


def lex(exp):  # Lex a single line
    lexr = lexer()  # Create a Lexer object

    lexr.add_token_expr(r'^[\s]', None)
    lexr.add_token_expr(r'^[0-9]+(\.[0-9]+)?', NUM)
    lexr.add_token_expr(r'^[()]', PAREN)
    lexr.add_token_expr(r'^(\+|-|/|\*|%|^)', OP)

    return lexr.lex(exp)