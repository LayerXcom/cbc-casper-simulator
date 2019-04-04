from cbc_casper_simulator.examples.broadcast import simulate as broadcast
from cbc_casper_simulator.examples.lmd_ghost import simulate as lmd_ghost
import argparse

parser = argparse.ArgumentParser(description='CBC Casper Simulator')
parser.add_argument(
    '--example', help='broadcast or lmd_ghost', default='broadcast')
args = parser.parse_args()

if args.example == 'broadcast':
    broadcast()
elif args.example == 'lmd_ghost':
    lmd_ghost()
else:
    print("Error: argument is invalid")
