"""
Class that oversees the lexers and stores the tokens long term.

"""
import sys
from scanner import Scanner

class Lexer(object):

    def __init__(self, path_to_file):
        self.path = path_to_file

    def execute(self):
        with open(self.path, 'r') as sourceFile:
            sourcecode = sourceFile.read()

        scan = Scanner(sourcecode)
        self.tokens = scan.scanTokens()


# Should only be main program if testing lexer
if __name__ == "__main__":
    lex = Lexer(sys.argv[1])
    lex.execute()
    for tok in lex.tokens:
        print(str(tok))
