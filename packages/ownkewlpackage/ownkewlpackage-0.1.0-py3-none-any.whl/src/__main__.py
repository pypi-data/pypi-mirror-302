import os
import argparse
from . import hello

parser = argparse.ArgumentParser(description = "Hello from test env.")
parser.add_argument('-l', '--lines', nargs = '+', help = 'num lines to show')
parser.add_argument('-w', '--words', action = 'store_true', help='word')
parser.add_argument('-c', '--chars', action = 'store_true', help='char')
parser.add_argument('files', nargs = '+', help = 'add n files')

args = parser.parse_args()
hello()
if args.lines and args.files:
    print(f'lines: {args.lines} files: {args.files}')

for f in args.files:
    print(f)
    if args.lines:
        print('action with line')
