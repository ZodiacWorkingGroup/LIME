import sys
from defusedxml.ElementTree import fromstring, parse

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = input('Filename: ')

try:
    root = parse(fn).getroot()
    print(root)
except FileNotFoundError:
    try:
        root = parse(fn+'.xml').getroot()
        print(root)
    except FileNotFoundError:
        print('File '+fn+'not found!')
