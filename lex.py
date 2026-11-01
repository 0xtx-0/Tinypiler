import enum
import sys

#The tokenType enum contains all the valid tokens that our language allows
class tokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    #Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    #Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

class Lexer:
    def __init__(self, source):
        self.source = source + '\n'  #source code to lex as a string
        self.curChar = ' '           #current character in the string
        self.curPos = -1             #current position in the string
        self.nextChar()

    #Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar =  '\0'  #EOF
        else:
            self.curChar = self.source[self.curPos]

    #Return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    #for invalid tokens, print error message and exit
    def abort(self, message):
        sys.exit("Lexical error: " + message)

    #skip whitespace except newlines
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    #skip comments in the code
    def skipComment(self):
        pass

    #return the next token
    #This function classifies some commonly used tokens(symbols)
    def getToken(self):
        self.skipWhitespace()
        if self.curChar == '+':
            token = Token(self.curChar, tokenType.PLUS)
        elif self.curChar == '-': 
            token = Token(self.curChar, tokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, tokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, tokenType.SLASH)
        elif self.curChar == '=':
            if self.peek() == '=':          #peek() allows looking at the next char w/o discarding current one
                lastChar = self.curChar     #which allows checking operators like ==, >=and <=
                self.nextChar()
                token = Token(lastChar + self.curChar, tokenType.EQEQ)
            else:
                token = Token(self.curChar, tokenType.EQ)
        elif self.curChar == '>':
            #check whether this token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, tokenType.GTEQ)
            else:
                token = Token(self.curChar, tokenType.GT)
        elif self.curChar == '<':
                #check whether this token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, tokenType.LTEQ)
            else:
                token = Token(self.curChar, tokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, tokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\n':                          #End of Line
            token = Token(self.curChar, tokenType.NEWLINE)
        elif self.curChar == '\0':                          #End of File
            token = Token('', tokenType.EOF)
        else:                                               #invalid token
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token
        
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  #The token's actual text(to be used by identifiers, strings and numbers)
        self.kind = tokenKind  #The type that the token is classified as
