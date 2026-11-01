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
        pass

    #skip whitespace except newlines
    def skipWhitespace(self):
        pass

    #skip comments in the code
    def skipComment(self):
        pass

    #return the next token
    def getToken(self):
        pass
