
import argparse

parser = argparse.ArgumentParser(
    description='Performs some useful work.',
)

parser.add_argument(
    '--toggle', '-t',
    #type=bool,
    default=False,
    #nargs='?',
    action='store_true', #means that if -t is passed set to True
    help='a boolean toggle',
)

args = parser.parse_args()
print(f"toggle arg: {args.toggle}")
