import argparse

parser = argparse.ArgumentParser(
    description='Performs some useful work.',
)

parser.add_argument(
    '--age',
    type=int,
    default='35',
    nargs='?',
    help='age, an optional positional argument',
)

args = parser.parse_args()
print(f"second arg: {args.age}")
