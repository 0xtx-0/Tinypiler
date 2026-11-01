## Basic structure:

source code -> Lexer -> Parser -> Emitter -> Compiled code 

### The grammar for the Parser
The parser needs a clearly defined set of grammar rules to check syntax of the programs

1. Statements, since all programs will contain >= 1 statement(s)
  `program ::= {statement}`

2. The statements of the program will involve keywords we defined in ./lex.py 
   These include:
   - PRINT (for printing to the console)
   - Or IF, THEN & ENDIF (to handle conditional control flow)
   - Or WHILE & REPEAT (for loops) and ENDWHILE (to terminate loops)
   - Or LABEL (for declaration of identifiers)
   - Or GOTO (jumps in programs)
   - Or LET (for variable definition)
   - Or INPUT (for accepting user input)

3. And then some logical and arithmetic operators holding those statements

The grammar for the parser looks something like this:
```
program ::= {statement}
statement ::= "PRINT" (expression | string) nl
    | "IF" comparison "THEN" nl {statement} "ENDIF" nl
    | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
    | "LABEL" ident nl
    | "GOTO" ident nl
    | "LET" ident "=" expression nl
    | "INPUT" ident nl
comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
expression ::= term {( "-" | "+" ) term}
term ::= unary {( "/" | "*" ) unary}
unary ::= ["+" | "-"] primary
primary ::= number | ident
nl ::= '\n'+
```


Now, for each rule in the grammar, we need a function in parser that checks for it. Pretty simple so far

#### Parsing expressions
This part is slightly tricky because we also have to keep operator precedence in mind while parsing mathematical expressions. Meanwhile, comparisons and expressions with unary operators can be parsed as-is.

To achieve different levels of precedence, we organise the grammar rules sequencially. The operators with higher precedence will be placed lower in the grammar rule so that the ones with lower precedence are processed first. eg:
    (a+b-c) * d
    the grammar rule definition will follow the order: rule(+,-) -> rule(*,/)
