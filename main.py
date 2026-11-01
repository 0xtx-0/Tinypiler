from lex import *

def main():
    source = "DOES IT WORK??"
    lexer = Lexer(source)

    while lexer.peek() != '\0':
        print(lexer.curChar)
        lexer.nextChar()

main()
