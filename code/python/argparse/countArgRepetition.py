import argparse

parser = argparse.ArgumentParser(
    description='restict argument values',
)

parser.add_argument(
    "-v", "--verbosity",
    action="count",
    help='increase verbosity',
)

args = parser.parse_args()
print(f"verbosity count: {args.verbosity}")
