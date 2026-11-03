class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    def emit(self,code):   # for appending the code
        self.code += code

    def emitLine(self, code):   # for adding a newline after each statement
        self.code += code + '\n'

    def headerLine(self, code):   # for adding c headers on top of the output file
        self.header += code + '\n'

    def writeFile(self):       # write the generated code to a file
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)

