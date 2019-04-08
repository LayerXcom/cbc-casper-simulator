from cbc_casper_simulator.examples.simple import run as simple_run
import argparse


def main():
    parser = argparse.ArgumentParser(description='CBC Casper Simulator')
    parser.add_argument(
        '-i', '--input', help='The file path of simulation parameters.'
    )
    parser.add_argument(
        '-o', '--output', help='The file path to output simulation result.'
    )
    args = parser.parse_args()
    simple_run(args.input, args.output)


if __name__ == "__main__":
    main()
