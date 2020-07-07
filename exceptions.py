"""
Hols our intepreter exceptions
"""
class ParserException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class RuntimeException(Exception):
    def __init__(self, msg, token):
        Exception.__init__(self, msg)
        self.token = token
