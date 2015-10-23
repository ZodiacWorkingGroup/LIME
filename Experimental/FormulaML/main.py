import sys
from defusedxml.ElementTree import fromstring, parse

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = input('Filename: ')

root = parse(fn).getroot()
print(root)
