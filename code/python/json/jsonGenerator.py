import argparse


class JsonVarsTemplateGeneratorConstants:
    SRC_FILE = 'src.json'
    TRANSLATION_FILE = 'trans.json'

class JsonVarsTemplateGenerator:
    source_file = JsonVarsTemplateGeneratorConstants.SRC_FILE
    trans_file = JsonVarsTemplateGeneratorConstants.TRANSLATION_FILE
    translations = {}

    def __init__(self, cli_args):
        if cli_args.file:
            self.source_file = cli_args.file
        if cli_args.trans:
            self.trans_file = cli_args.trans

    def printMe(self):
        print(f"jsonVarsTemplateGenerator instance with source_file={self.source_file}, trans_file={self.trans_file}")

    def load_translations()
        with open(self.source_file, "r") as src_file:
            pass
        

def help():
    msg = """This utility replaces vars with values 
It receives two arguments. Source file containing a valid json and a translations file, containing a var:value pairs json for 
the replacement
A var is identified by doubly enclosing curly braces. e.g. {{var}} 
Please provide the two arguments -f <source file> -t <translations file> 
    """
    #print(msg)
    return msg

def get_args():
    parser = argparse.ArgumentParser(usage='-f <source file> -t <translations file>', description='A utility for replacing json vars, enclosed by curly braces. e.g. {{var}} vars with values')
    parser.add_argument(
            "-f", "--file",
            type=str,
            default='src.json',
            help='File containing json with vars enclosed by doubly curly braces to be replaced'
            )
    parser.add_argument(
            "-t", "--trans",
            type=str,
            default='trans.json',
            help='File containing json with key:value pairs for use when replacing {{vars}} in source json file'
            )
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    print(f"got args {args}")
    jsonVarsTemplateGenerator = JsonVarsTemplateGenerator(args)
    jsonVarsTemplateGenerator.printMe()

if __name__ == "__main__":
    main()
