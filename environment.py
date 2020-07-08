"""
Class that mangages runtime environment of sython.
"""
import exceptions

class Environment(object):

    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise exceptions.RuntimeException("Undefined variable " + name.lexeme)
