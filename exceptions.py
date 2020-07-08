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

    def __str__(self):
        if self.token:
            return "%d %s" % (self.token.line, self.msg)
        return self.msg
