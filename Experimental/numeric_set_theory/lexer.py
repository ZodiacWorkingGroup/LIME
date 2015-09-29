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
