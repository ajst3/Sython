"""
Classes for scanning and lexer error reporting.
"""

class Scanner(object):
    """ Class for scanner used by the lexer to form tokens and such. """

    def __init__(self, source):
        self.source = source
        self.current = 0
        self.start = 0
        self.line = 1
        self.tokenList = []
        self.keywords = ['and', 'class', 'else', 'false', 'true', 'for',
                         'def', 'if', 'nil', 'or', 'return',
                         'super', 'this', 'while', 'num', 'str', 'boolean']

    def scanTokens(self):
        """ Scans tokens in the source code and returns a list of tokens."""
        while not self._atEnd():
            self.start = self.current
            self._scanToken()

        self.tokenList.append(Token("EOF", "", None, self.line))
        return self.tokenList

    def _atEnd(self):
        """ Determines if we are at end of file."""
        return self.current >= len(self.source)

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _addToken(self, type, literal=None):
        self.tokenList.append(Token(type,
            self.source[self.start:self.current], literal, self.line))

    def _match(self, c):
        if self._atEnd():
            return False
        if self.source[self.current] == c:
            self.current += 1
            return True
        else:
            return False

    def _peek(self):
        if self._atEnd():
            return '\0'
        return self.source[self.current]

    def _isWhitespace(self, c):
        return c == ' ' or c == '\t' or c == '\r' or c == '\n'

    def _string(self):
        while self._peek() != '"' and not self._atEnd():
            if self._peek() == '\n':
                err = Error(self.line, "Unterminated string")
                err.report()
                return
            self._advance()

        if self._atEnd():
            err = Error(self.line, "Unterminated string")
            err.report()
            return
        self._advance()
        val = self.source[self.start+1: self.current-1]
        self._addToken(TokenType('STRING'), val)

    def _isDigit(self, c):
        return c.isnumeric()

    def _peekNext(self):
        if self.current + 1 > len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _number(self):
        while self._isDigit(self._peek()):
            self._advance()
        if self._peek() == '.' and self._isDigit(self._peekNext()):
            self._advance()
        while self._isDigit(self._peek()):
            self._advance()
        type = TokenType("NUMBER")
        self._addToken(type, float(self.source[self.start:self.current]))

    def _isAlpha(self, c):
        return c.isalpha()

    def _isAlphaNumeric(self, c):
        return c.isalnum()

    def _identifier(self):
        while self._isAlphaNumeric(self._peek()):
            self._advance()
        val = self.source[self.start:self.current]
        if val in self.keywords:
            type = val.upper()
        else:
            type = TokenType("IDENTIFIER")
        self._addToken(type)

    def _scanToken(self):
        c = self._advance()
        if c == '(':
            type = TokenType("LEFT_PAREN")
            self._addToken(type)
        elif c == ')':
            type = TokenType("RIGHT_PAREN")
            self._addToken(type)
        elif c == '{':
            type = TokenType("LEFT_BRACE")
            self._addToken(type)
        elif c == '}':
            type = TokenType("RIGHT_BRACE")
            self._addToken(type)
        elif c == ',':
            type = TokenType("COMMA")
            self._addToken(type)
        elif c == '.':
            type = TokenType("DOT")
            self._addToken(type)
        elif c == '-':
            type = TokenType("MINUS")
            self._addToken(type)
        elif c == '+':
            type = TokenType("PLUS")
            self._addToken(type)
        elif c == "/":
            type = TokenType("SLASH")
            self._addToken(type)
        elif c == "*":
            type = TokenType("STAR")
            self._addToken(type)
        elif c == ";":
            type = TokenType("SEMICOLON")
            self._addToken(type)
        elif c == '!':
            if self._match('='):
                type = TokenType("BANG_EQUAL")
            else:
                type = TokenType("EQUAL")
            self._addToken(type)
        elif c == "=":
            if self._match('='):
                type = TokenType("EQUAL_EQUAL")
            else:
                type = TokenType("EQUAL")
            self._addToken(type)
        elif c == "<":
            if self._match('='):
                type = TokenType("LESS_EQUAL")
            else:
                type = TokenType("LESS")
            self._addToken(type)
        elif c == ">":
            if self._match('='):
                type = TokenType("GREATER_EQUAL")
            else:
                type = TokenType("GREATER")
            self._addToken(type)
        elif c == "#":
            # advance to next line
            while not self._peek() != '\n' and not self._atEnd():
                self._advance()
        elif self._isWhitespace(c):
            if c == '\n':
                self.line += 1
        elif c == '"':
            self._string()
        else:
            if self._isDigit(c):
                self._number()
            elif self._isAlpha(c):
                self._identifier()
            else:
                err = Error(self.line, ("Invalid Token!  %s" % c))
                err.report()


class Error(object):
    """ Class for reporting lexer error."""

    def __init__(self, line, msg):
        self.line = line
        self.msg = msg

    def report(self):
        print("Line %d, %s" % (self.line, self.msg))


class TokenType(object):
    """ Describes the type of token."""

    def __init__(self, type):
        self.types = \
        ["LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
          "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",
          "BANG", "BANG_EQUAL",
          "EQUAL", "EQUAL_EQUAL",
          "GREATER", "GREATER_EQUAL",
          "LESS", "LESS_EQUAL",
          "IDENTIFIER", "STRING", "NUMBER",
          "AND", "CLASS", "ELSE", "FALSE", "DEF", "FOR", "IF", "NIL", "OR",
          "RETURN", "SUPER", "THIS", "TRUE", "WHILE", "NUM", "STR", "BOOLEAN",
          "EOF"
          ]
        self.name = type

    def is_valid(self):
        return self.name in self.types

    def __str__(self):
        return self.name


class Token(object):
    """ Represents token in source code."""

    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "Type = %s    lexeme = %s     literal = %s    line = %d" % \
        (self.type, self.lexeme, str(self.literal), self.line)
