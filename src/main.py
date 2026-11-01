from lex import *
from parser import *
import sys

def main():
    print("Tinypiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # Initialize the lexer and parser.
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program() # Start the parser.
    print("Parsing completed.")

main()
