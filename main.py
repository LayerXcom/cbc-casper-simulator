# NOTE: Do not create png files for now
# from cbc_casper_simulator.examples.broadcast import simulate as broadcast
# from cbc_casper_simulator.examples.lmd_ghost import simulate as lmd_ghost
from cbc_casper_simulator.examples.simple import run as simple_run
import argparse

parser = argparse.ArgumentParser(description='CBC Casper Simulator')
parser.add_argument(
    '-i', '--input', help='The file path of simulation parameters.'
)
parser.add_argument(
    '-o', '--output', help='The file path to output simulation result.'
)
args = parser.parse_args()
"""
parser.add_argument(
    '--example', help='broadcast or lmd_ghost', default='broadcast')


if args.example == 'broadcast':
broadcast()
elif args.example == 'lmd_ghost':
    lmd_ghost()
"""
simple_run(args.input, args.output)
