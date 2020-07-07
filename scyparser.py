"""
Class that is used to parse the list of tokens.
"""
import exceptions
import expressions as exp
from error_reporting import Error
from scanner import Token, TokenType

class Parser(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """ Parses an expression an returns it."""
        try:
            return self.expression()
        except exceptions.ParserException:
            return None

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self._match("BANG_EQUAL", "EQUAL_EQUAL"):
            # Operator is the previous one since we consumed the token in match
            operator = self._previous()

            # Get the right side of the cquality
            right = self.comparison()

            # Create binary expression ast node
            expr = expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.addition()

        while self._match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self._previous()
            right = self.addition()
            expr = exp.Binary(expr, operator, right)
        return expr

    def addition(self):
        expr = self.multiplication()

        while self._match("MINUS", "PLUS"):
            operator = aelf._previous()
            right = self.multiplication()
            expr = exp.Binary(expr, operator, right)
        return expr

    def multiplication(self):
        expr = self.unary()

        while self._match("SLASH", "STAR"):
            operator = self._previous()
            right = self.unary()
            expr = exp.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self._match("BANG", "MINUS"):
            operator = self._previous()
            right = self.unary()
            return exp.Unary(operator, right)
        return self.primary()

    def primary(self):
        if self._match("FALSE"):
            return exp.Literal(False)
        if self._match("TRUE"):
            return exp.Literal(True)
        if self._match("NIL"):
            return exp.Literal(None)
        if self._match("STRING", "NUMBER"):
            return exp.Literal(self._previous().literal)
        if self._match("LEFT_PAREN"):
            expr = self.expression()
            self._consume("RIGHT_PAREN", "Expected ')' after expression")
            return exp.Grouping(expr)
        raise self.error(self._peek(), "Expected expression")

    def error(self, token, msg):
        Error().error(token, msg)
        return exceptions.ParserException(msg)

    def synchronize(self):
        """ Consumes tokens until statement boundary reached."""
        self._advance()

        while not self._isAtEnd():
            if self._previous().type == "SEMICOLON":
                return
            to_return = ["CLASS", "FUN", "VAR", "FOR", "IF", "WHILE",
            "RETURN"]
            if self._peek().type in to_return:
                return
            self._advance()

    def _consume(self, type, msg):
        if self._check(type):
            return self._advance()
        raise self.error(self._peek(), msg)

    def _match(self, *types):
        """ Iterates through tokens and determines if they
        match the given types."""
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _check(self, type):
        if self._isAtEnd():
            return False
        return str(self._peek().type) == type

    def _advance(self):
        if not self._isAtEnd():
            self.current += 1
        return self._previous()

    def _isAtEnd(self):
        return self._peek() == "EOF"

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current-1]
