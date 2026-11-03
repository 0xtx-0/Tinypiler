# Tinypiler

A small compiler written to learn the basics of compilers

```
Tiny source (.tn) -> Lexer -> Parser -> Emitter -> C source (out.c) -> executable
```

## Requirements

- Python 3
- GCC (or another C compiler, if you edit `build.sh`)


## Quick start

The `build.sh` script compiles a `.tn` file to C, then compiles that C with GCC:

```sh
./build.sh examples/fibonacci.tn
./fibonacci
```

The script writes `fibonacci.c` and the `fibonacci` executable into the current
directory.

To compile every example at once, run `build.sh` with no arguments:

```sh
./build.sh
```


## Language guide

A Tiny program is a sequence of statements, one per line. Indentation is ignored.
Blank lines are allowed. Comments start with `#` and run to the end of the line.

### Variables and input

```tn
LET x = 10
LET y = x * 2 + 1
INPUT name
```

All variables are 32-bit floats. `INPUT` reads a number from standard input; if the
input is not a valid number, the variable is set to `0` and the rest of the line is
discarded. A variable must be assigned with `LET` or `INPUT` before it is used.

### Printing

Print a string literal:

```tn
PRINT "Hello, world!"
```

Print an expression (formatted to two decimal places):

```tn
PRINT x * 3
```

### Conditionals

```tn
IF x > 10 THEN
    PRINT "big"
ENDIF
```

### Loops

```tn
LET i = 0
WHILE i < 5 REPEAT
    PRINT i
    LET i = i + 1
ENDWHILE
```

### Labels and jumps

```tn
LABEL loop
PRINT "again"
GOTO loop
```

`GOTO` may only target a label that is declared somewhere in the program.


### Operators

| Category    | Operators                        |
| ----------- | -------------------------------- |
| Arithmetic  | `+` `-` `*` `/`                  |
| Unary       | `+` `-`                          |
| Comparison  | `==` `!=` `<` `<=` `>` `>=`      |


### Keywords

`LABEL`, `GOTO`, `PRINT`, `INPUT`, `LET`, `IF`, `THEN`, `ENDIF`, `WHILE`, `REPEAT`,
`ENDWHILE`

## Complete example

`examples/fibonacci.tn`:

```tn
PRINT "How many fibonacci numbers do you want?"
INPUT nums
PRINT ""

LET a = 0
LET b = 1
WHILE nums > 0 REPEAT
    PRINT a
    LET c = a + b
    LET a = b
    LET b = c
    LET nums = nums - 1
ENDWHILE
```

```sh
./build.sh examples/fibonacci.tn
./fibonacci
```


## Project layout

```
tinypiler/
├── src/
│   ├── tiny.py
│   ├── emitter.py
│   ├── lexer.py
│   ├── parser.py
│   └── ...
├── examples/
│   ├── average.tn
│   └── fibonacci.tn
├── README.md
└── build.sh
```
