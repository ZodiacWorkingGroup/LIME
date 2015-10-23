from UtopiaLexer import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support

# Tags
BRACK = 'BRACKET'
SEP = 'SEPARATOR'
NUM = 'NUMBER'
OP = 'OP'
ST = 'SUCH_THAT'


def lex(script):
    lexr = lexer()

    lexr.add_token_expr(r'^[{}]', BRACK)
    lexr.add_token_expr(r'^,', SEP)
    lexr.add_token_expr(r'^[0-9]+(\.[0-9]+)?', NUM)
    lexr.add_token_expr(r'^(?|?|?)', OP)
    lexr.add_token_expr(r'^:', ST)