import sys
from lex import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set()         # variables declared so far
        self.labelsDeclared = set()  # labels declared so far
        self.labelsGotoed = set()    # labels on which goto has been performed so far

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error! " + message)

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        #skip excess newlines
        while self.checkToken(tokenType.NEWLINE):
            self.nextToken()

        # parse all statements in the program
        while not self.checkToken(tokenType.EOF):
            self.statement()

        # check if each GOTO label is declared
        for label in labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

    def statement(self):
        # Check the first token to see what kind of statement this is.

        # "PRINT" (expression | string)
        if self.checkToken(tokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(tokenType.STRING):
                # Simple string.
                self.nextToken()
            else:
                # Expect an expression.
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(tokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(tokenType.THEN)
            self.nl()

            # Zero or more statements in the body.
            while not self.checkToken(tokenType.ENDIF):
                self.statement()

            self.match(tokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(tokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(tokenType.REPEAT)
            self.nl()

            # Zero or more statements in the loop body.
            while not self.checkToken(tokenType.ENDWHILE):
                self.statement()

            self.match(tokenType.ENDWHILE)

        # "LABEL" ident
        elif self.checkToken(tokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()

            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.match(tokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(tokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.match(tokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(tokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()

            #check if ident exists in symbol table, if not then declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(tokenType.IDENT)
            self.match(tokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(tokenType.INPUT):
            self.nextToken()

            # if variable doesn't already exist, declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(tokenType.IDENT)

        # Error handling for invalid statements
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")
        self.nl()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

            # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):
        return self.checkToken(tokenType.GT) or self.checkToken(tokenType.GTEQ) or self.checkToken(tokenType.LT) or self.checkToken(tokenType.LTEQ) or self.checkToken(tokenType.EQEQ) or self.checkToken(tokenType.NOTEQ)


     # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(tokenType.PLUS) or self.checkToken(tokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(tokenType.ASTERISK) or self.checkToken(tokenType.SLASH):
            self.nextToken()
            self.unary()


    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(tokenType.PLUS) or self.checkToken(tokenType.MINUS):
            self.nextToken()        
        self.primary()

    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(tokenType.NUMBER): 
            self.nextToken()
        elif self.checkToken(tokenType.IDENT):
            # Ensure a variable already exists
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)
            self.nextToken()
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)

     # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")
		
        # Require at least one newline.
        self.match(tokenType.NEWLINE)
        # But we will allow extra newlines too, of course.
        while self.checkToken(tokenType.NEWLINE):
            self.nextToken()
