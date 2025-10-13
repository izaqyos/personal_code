import argparse

parser = argparse.ArgumentParser(
    description='Performs some useful work.',
)

# Put your add_argument calls here
# parser.add_argument(...)

args = parser.parse_args()
print(args)
#print(args.some_param)
