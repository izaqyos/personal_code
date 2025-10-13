import argparse

parser = argparse.ArgumentParser(
    description='Performs some useful work.',
)

parser.add_argument(
    'name',
    type=str,
    default='yosi',
    nargs='?',
    help='name, a positional argument',
    #metavar='ARG',
)
parser.add_argument(
    'age',
    type=int,
    default='35',
    nargs='?',
    help='age, a positional argument',
)

#args = parser.parse_args([])  # Namespace(arg='arg_default')
#print(f"args from default Namespace: {args}")
#args = parser.parse_args(['name'])  # Namespace(arg='value')
#print(f"args from name arg Namespace: {args.name}")
args = parser.parse_args()
print(f"single arg: {args.name}")
print(f"second arg: {args.age}")
