"""
Class that is used to evaulate expressions by using the visitor pattern.
Implements the runtime world.
"""
from handling import exceptions
from handling.error_reporting import Error
from handling.environment import Environment

class Interpreter(object):

    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements):
        """ For each statement given to us by the parser
        we execute the statement."""
        # If there is a null reference in statements,
        # there was a parser error. So dont run anything.
        if None in statements:
            return

        try:
            for statement in statements:
                self.execute(statement)
        except exceptions.RuntimeException as eee:
            Error().runtimeError(eee)

    def execute(self, stmt):
        """ Begin visitor pattern to evaluate the subexpressions."""
        stmt.accept(self)

    def executeBlock(self, statements, environment):
        # Save previous env
        previous_env = self.environment

        try:
            # Set env for this block
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        except exceptions.RuntimeException as eee:
            # Reraise as it will be caught in interpret method
            raise
        finally:
            # Restore previous env
            self.environment = previous_env

    # Functions for visiting statements
    def visitIf(self, stmt):
        if self._isTruthy(self._evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visitVar(self, stmt):
        """ Evaluate visitor statement by putting
        the var name in the dictionary with the evaluated initializer."""
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, stmt.type, value)

    def visitBlock(self, stmt):
        """ Execute statements in block."""
        self.executeBlock(stmt.statements, Environment(self.environment))

    def visitExpression(self, stmt):
        """ Return the value of the evaluated expression."""
        self._evaluate(stmt.expression)

    def visitPrint(self, stmt):
        """ Evaluate the expression and print the result."""
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    # Functions for visiting expressions
    def visitVariable(self, expr):
        """ Return the value of the variable the
        expression is referencing."""
        return self.environment.get(expr.name)

    def visitAssign(self, expr):
        value = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitLiteral(self, expr):
        # Pull value out of the tree node
        return expr.val

    def visitGrouping(self, expr):
        """ Evauluate expression in the parens."""
        return self._evaluate(expr.expression)

    def visitUnary(self, expr):
        """ Evaluate the expression on the right of the unary op."""
        right = self._evaluate(expr.right)

        if str(expr.operator.type) == "MINUS":
            self._checkNumberOperand(expr.operator, right)
            return -1 * float(right)
        if str(expr.operator.type) == "BANG":
            return not self._isTruthy(right)

        # Could not reach end
        return None

    def visitBinary(self, expr):
        """ Evaluate the expressions on the left and right of
        the operator, then perform the operation on them."""
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        op = str(expr.operator.type)

        # Math operator
        if op == "MINUS":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) - float(right)
        if op == "PLUS":
            if isinstance(right, str) and isinstance(left, str):
                return str(left) + str(right)
            if isinstance(right, float) and isinstance(left, float):
                return float(left) + float(right)
            raise exceptions.RuntimeException("Operands must be two numbers"
                                              " or two strings", expr.operator)
        if op == "STAR":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) * float(right)
        if op == "SLASH":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) / float(right)

        # Comparison operator
        if op == "GREATER":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) > float(right)
        if op == "GREATER_EQUAL":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) >= float(right)
        if op == "LESS":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) < float(right)
        if op == "LESS_EQUAL":
            self._checkNumbersOperand(expr.operator, left, right)
            return float(left) <= float(right)

        # Equality operators
        if op == "BANG_EQUAL":
            return not self._isEqual(left, right)
        if op == "EQUAL_EQUAL":
            return self._isEqual(left, right)

    def _evaluate(self, expr):
        # Recursively working through the expressions
        # using the visitor patterns
        return expr.accept(self)

    def _isTruthy(self, val):
        # All nonzero, nonnull values are true, empty strings are false
        if val == None:
            return False
        if val == 0:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            if val == "":
                return False
        return True

    def _isEqual(self, left, right):
        if left == None and right == None:
            return True
        if left == None:
            return False

        return left == right

    def _checkNumberOperand(self, op, operand):
        if isinstance(operand, float):
            return
        raise exceptions.RuntimeException("Operand must be a number!", op)

    def _checkNumbersOperand(self, op, operand1, operand2):
        if isinstance(operand1, float) and isinstance(operand2, float):
            return
        raise exceptions.RuntimeException("Operands must be numbers!", op)

    def _stringify(self, x):
        if x is None:
            return "nil"
        if isinstance(x, int):
            return x
        if isinstance(x, float):
            text = str(x)
            if text[len(text)-2: len(text)] == ".0":
                return text[0:len(text)-2]
        if x is True:
            return "true"
        if x is False:
            return "false"
        return str(x)  # rely on object __str__ method
