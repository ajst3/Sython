"""
Hols our intepreter exceptions
"""
class ParserException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
