"""
Class that is used to parse the list of tokens. From the precendence
"""
from handling import exceptions
from tree import expressions as exp
from tree import stmt
from handling.error_reporting import Error
from tree.scanner import Token, TokenType

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
        if self._match("IF"):
            return self.ifstatement()

        if self._match("PRINT"):
            return self.printStatement()

        if self._match("WHILE"):
            return self.whilestatement()

        if self._match("DO"):
            return self.dostatement()

        if self._match("UNTIL"):
            return self.untilstatement()

        if self._match("FOR"):
            return self.forstatement()

        if self._match("LEFT_BRACE"):
            return stmt.Block(self.block())

        return self.expressionStatement()

    def ifstatement(self):
        self._consume("LEFT_PAREN", "Expected left paren after if")
        condition = self.expression()
        self._consume("RIGHT_PAREN", "Expected righ paren after condition")

        then_branch = self.statement()
        else_branch = None
        if self._match("ELSE"):
            else_branch = self.statement()

        return stmt.If(condition, then_branch, else_branch)

    def forstatement(self):
        self._consume("LEFT_PAREN", "Expected left paren after for")

        # Get the initializer
        if self._match("SEMICOLON"):  # No initializer
            initializer = None
        else:  # initializer is an assignment
            initializer = self.expressionStatement()

        # Get condition
        if self._check("SEMICOLON"):
            condition = None
        else:
            condition = self.expression()
        self._consume("SEMICOLON", "Expected semicolon after condition")

        # Get increment
        if self._check("RIGHT_PAREN"):
            increment = None
        else:
            increment = self.expression()

        self._consume("RIGHT_PAREN", "Expected ')' after clauses")

        body = self.statement()

        # Get else branch, which executes if the loop does not complete
        if self._match("ELSE"):
            else_branch = self.statement()
        else:
            else_branch = None
        return stmt.For(initializer, condition, body,increment, else_branch)

    def whilestatement(self):
        self._consume("LEFT_PAREN", "Expected left paren after while")
        condition = self.expression()
        self._consume("RIGHT_PAREN", "Expected right paren after condition")

        body = self.statement()
        return stmt.While(condition, body)

    def untilstatement(self):
        self._consume("LEFT_PAREN", "Expected left paren after until")
        condition = self.expression()
        self._consume("RIGHT_PAREN", "Expected right paren after until")

        body = self.statement()
        return stmt.Until(condition, body)

    def dostatement(self):
        # This is the block immediately following the do statement
        body = self.statement()

        # Get condition
        er = self._consume("WHILE", "Expected while after do block", True)
        et = self._consume("UNTIL", "Expected while after do block", True)
        if not er and not et:
            raise self.error(self._peek(),
                             "Expected while or until after do block")

        self._consume("LEFT_PAREN", "Expected left paren after while/until")
        condition = self.expression()
        self._consume("RIGHT_PAREN", "Expected right paren after condition")
        if er:
            return stmt.Do(condition, body, "while")
        else:
            return stmt.Do(condition, body, "until")

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
        expr = self.ore()

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

    def ore(self):
        expr = self.andd()
        while self._match("OR"):
            op = self._previous()
            right = self.andd()
            expr = exp.Logical(expr, op, right)
        return expr

    def andd(self):
        expr = self.equality()
        while self._match("AND"):
            op = self._previous()
            right = self.equality()
            expr = exp.Logical(expr, op, right)
        return expr

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

    def _consume(self, type, msg, silent=False):
        if self._check(type):
            return self._advance()
        if not silent:
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
