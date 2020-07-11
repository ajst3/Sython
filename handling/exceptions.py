"""
Hols our intepreter exceptions
"""
class ParserException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class RuntimeException(Exception):
    def __init__(self, msg, token=None):
        Exception.__init__(self, msg)
        self.token = token
        self.msg = msg

    def __str__(self):
        if self.token:
            return "Line %d %s" % (self.token.line, self.msg)
        return self.msg
