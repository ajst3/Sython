"""
Main program to execute Sython code.
"""
from lexer import Lexer
from syinterpreter import Interpreter
from syparser import Parser
from ast_printer import Printer

class Sython(object):
    def __init__(self, path_to_file=None):
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
            exp_tree = par.parse()
            if not exp_tree:
                return
            # printer = Printer()
            # print(printer.printExp(exp_tree))
            self.interpreter.interpret(exp_tree)

if __name__ == "__main__":
    sy = Sython()
    author_info = (" Welcome to the Sython shell, where you can script in "
    "Sython. Authored by Austin Tercha")
    print(author_info)
    uinput = input(">>> ")
    while uinput != "quit":
        uinput = input(">>> ")
        sy.execute(uinput)
