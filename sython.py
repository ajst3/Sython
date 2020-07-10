"""
Main program to execute Sython code.
"""
import sys
from lexer import Lexer
from syinterpreter import Interpreter
from syparser import Parser
from ast_printer import Printer

class Sython(object):
    def __init__(self, path_to_file=None):
        """ Define path_to_file if running a script."""
        self.lex = Lexer(path_to_file)
        self.interpreter = Interpreter()

    def execute(self, source=None):
        # We are running the shell
        if source:
            self.lex.execute(source)
            tokens = self.lex.tokens
            # for token in tokens:
            #     print(str(token))
            par = Parser(tokens)
            statements = par.parse()
            if not isinstance(statements, list):
                statements = [statements]
            self.interpreter.interpret(statements)
        else:
            self.lex.execute()
            # for token in self.lex.tokens:
            #     print(str(token))
            par = Parser(self.lex.tokens)
            statements = par.parse()
            if not statements:
                return
            if not isinstance(statements, list):
                statements = [statements]
            self.interpreter.interpret(statements)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sy = Sython(sys.argv[1])
        sy.execute()
    else:
        sy = Sython()
        author_info = (" Welcome to the Sython shell, where you can script in "
        "Sython. Authored by Austin Tercha")
        print(author_info)
        uinput = input(">>> ")
        sy.execute(uinput)
        while uinput != "quit":
            uinput = input(">>> ")
            sy.execute(uinput)
