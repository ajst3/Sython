"""
Class used to report errors
"""

class Error(object):

    def error(self, token, msg):
        if token.type == "EOF":
            self.report(token.line, "at end of file", msg)
        else:
            self.report(token.line, " at '" + token.lexeme + "'" + msg)

    def report(self, line, msg):
        print("Line %d, %s" % (line, msg))
