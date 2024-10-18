from .main import fromSource

from gamuLogger import Logger, LEVELS
import argparse

Logger.setModule("DiagramTool")


def buildArgParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='create a class diagram from source code')
    parser.add_argument('source', type=str, help='source code main file')
    parser.add_argument('output', type=str, help='output file')
    parser.add_argument('--debug', action='store_true', help='print debug information', default=False)
    parser.add_argument('--dump', action='store_true', help='dump parsed data to stdout', default=False)
    parser.add_argument('--save-ast', action='store_true', help='save ast to file', default=False)
    return parser


def getArgs() -> argparse.Namespace:
    parser = buildArgParser()
    args = parser.parse_args()
    return args

def main():
    args = getArgs()
    if args.debug:
        Logger.setLevel('stdout', LEVELS.DEBUG)
    
    try:
        fromSource(args.source, args.output, args.save_ast, args.dump, args.debug)
    except Exception as e:
        Logger.critical(f"An error occured")
        exit(1)
    
    
if __name__ == "__main__":
    main()