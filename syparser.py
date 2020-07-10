"""
Class that is used to parse the list of tokens. From the precendence
"""
import exceptions
import expressions as exp
import stmt
from error_reporting import Error
from scanner import Token, TokenType

class Parser(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """ Returns a list of statements."""
        try:
            statements = []
            while not self._isAtEnd():
                statements.append(self.declaration())
            return statements
        except exceptions.ParserException:
            return None

    def declaration(self):
        try:
            # Check if it is a variable declaration
            if self._match("NUM", "STR", "BOOL"):
                return self.varDelcaration()
            return self.statement()
        except exceptions.ParserException as eee:
            self.synchronize()
            return None

    def varDelcaration(self):
        vartype = self._previous()
        name = self._consume("IDENTIFIER", "Expected varibale name")
        initializer = None
        if self._match("EQUAL"):
            initializer = self.expression()
        self._consume("SEMICOLON", "Expected a ; after variable declaration")
        return stmt.Var(name, vartype, initializer)

    def statement(self):
        if self._match("PRINT"):
            return self.printStatement()

        if self._match("LEFT_BRACE"):
            return stmt.Block(self.block())

        return self.expressionStatement()

    def block(self):
        """ Returns a list of statements in the block."""
        statements = []
        while not self._check("RIGHT_BRACE") and not self._isAtEnd():
            statements.append(self.declaration())
        self._consume("RIGHT_BRACE", "Expected } to end block")
        return statements

    def printStatement(self):
        value = self.expression()
        self._consume("SEMICOLON", "Expected ; after value")
        return stmt.Print(value)

    def expressionStatement(self):
        expr = self.expression()
        self._consume("SEMICOLON", "Expected ; after value")
        return stmt.Expression(expr)

    def assignment(self):
        expr = self.equality()

        if self._match("EQUAL"):
            eq = self._previous()
            value = self.assignment()

            if isinstance(expr, exp.Variable):
                name = expr.name
                return exp.Assign(name, value)
            self.error(eq, "Invalid assignment")
        return expr

    def expression(self):
        return self.assignment()

    def equality(self):
        expr = self.comparison()

        while self._match("BANG_EQUAL", "EQUAL_EQUAL"):
            # Operator is the previous one since we consumed the token in match
            operator = self._previous()

            # Get the right side of the cquality
            right = self.comparison()

            # Create binary expression ast node
            expr = exp.Binary(expr, operator, right)
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
            operator = self._previous()
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
        if self._match("IDENTIFIER"):
            return exp.Variable(self._previous())
        raise self.error(self._peek(), " Expected expression")

    def error(self, token, msg):
        Error().error(token, msg)
        return exceptions.ParserException(msg)

    def synchronize(self):
        """ Consumes tokens until statement boundary reached."""
        self._advance()

        while not self._isAtEnd():
            if self._previous().type == "SEMICOLON":
                return
            to_return = ["CLASS", "DEF", "NUM", "FOR", "IF", "WHILE",
            "RETURN", "BOOL", "STR"]
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
        return str(self._peek().type) == "EOF"

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current-1]
