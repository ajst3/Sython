"""
Class that mangages runtime environment of sython.
"""
import exceptions

class Environment(object):

    def __init__(self, above=None):
        self.values = {}
        self.types = {}
        self.scopeAbove = above  # The environment (block) above this one

    def define(self, name, type, value):
        typetok = type
        type = typetok.type

        # Check that value type and vartype match
        # Uninitialized strs are nil, nums are 0 and bools are false
        if value is not None:
            if type.lower() == "str":
                if not isinstance(value, str):
                    raise exceptions.RuntimeException(
                        "Line %d Type error: not str" % typetok.line)
            if type.lower() == "num":
                if not (isinstance(value, int) or isinstance(value, float)):
                    raise exceptions.RuntimeException(
                        "Line %d Type error: not a num" % typetok.line)
            if type.lower() == "bool":
                if not isinstance(value, bool):
                    raise exceptions.RuntimeException(
                        "Line %d Type error not a bool" % typetok.line)
        else:
            if type.lower() == "num":
                value = 0
            elif type.lower() == "bool":
                value = False

        # Save variable type and value
        self.types[name] = type.lower()
        self.values[name] = value

    def assign(self, name, value):
        # Check that variable exists
        if self.scopeAbove:
            if not name.lexeme in self.values:
                self.scopeAbove.assign(name, value)
                return
        else:  # At the global level, if not here than var does not exist
            if not name.lexeme in self.values:
                raise exceptions.RuntimeException(
                    "Line %d Undefined variable %s" % (name.line, name.lexeme))

        # Variable is in this scope
        # Check type
        vtype = self.types[name.lexeme]
        if vtype == "num":
            if not (isinstance(value, int) or isinstance(value, float)):
                raise exceptions.RuntimeException("Line %d Type error: not num"
                                                  % name.line)
        if vtype == "str":
            if not isinstance(value, str):
                raise exceptions.RuntimeException("Line %d Type error: not str"
                                                  % name.line)
        if vtype == "bool":
            if not isinstance(value, bool):
                raise exceptions.RuntimeException("Line %d Type error: not bool"
                                                  % name.line)
        self.values[name.lexeme] = value

    def get(self, name):
        # Look for the variable in our scope/env
        if name.lexeme in self.values:
            # nums and bools can be accessed before being initialized
            # nothing else can
            varval = self.values[name.lexeme]
            vartype = self.types[name.lexeme]
            if (vartype != "num" or vartype != "bool") and \
                    (varval is None):
                raise exceptions.RuntimeException(
                    "Line %d Cannot access uninitialized variable" % name.line)
            return self.values[name.lexeme]

        # Did not find the variable in our scope so go up the chain
        if self.scopeAbove:
            return self.scopeAbove.get(name)

        # Variable is not defined in any scope
        raise exceptions.RuntimeException("Undefined variable " + name.lexeme)
