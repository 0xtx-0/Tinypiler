from lex import *

def main():
    source = "+- */> >= = != \n"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != tokenType.EOF:
        print(token.kind)
        token = lexer.getToken()
        
main()
