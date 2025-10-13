import argparse

parser = argparse.ArgumentParser(
    description='restict argument values',
)

parser.add_argument(
    "-l", "--levels",
    type=int,
    choices=[0,1,2,3],
    default=0,
    #nargs='?',
    help='choose a level',
)

args = parser.parse_args()
print(f"toggle arg: {args.levels}")
