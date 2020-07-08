"""
Class that is used to evaulate expressions by using the visitor pattern.
Implements the runtime world.
Note: To convert to static type think about adding a field to the expression
"""
import exceptions
from error_reporting import Error
from environment import Environment

class Interpreter(object):

    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except exceptions.RuntimeException as eee:
            Error().runtimeError(eee)

    def execute(self, stmt):
        stmt.accept(self)

    def visitVar(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitVariable(self, expr):
        return self.environment.get(expr.name)

    def visitExpression(self, stmt):
        self._evaluate(stmt.expression)

    def visitPrint(self, stmt):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    # Functions for visiting expressions
    def visitLiteral(self, expr):
        # Pull value out of the tree node
        return expr.val

    def visitGrouping(self, expr):
        return self._evaluate(expr.expression)

    def visitUnary(self, expr):
        right = self._evaluate(expr.right)

        if str(expr.operator.type) == "MINUS":
            self._checkNumberOperand(expr.operator, right)
            return -1 * float(right)
        if str(expr.operator.type) == "BANG":
            return not self._isTruthy(right)

        # Could not reach end
        return None

    def visitBinary(self, expr):
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
        # All nonzero, nonnull values are true
        if val == None:
            return False
        if val == 0:
            return False
        if val == False or val == True:
            return val
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
        if x == None:
            return "nil"
        if isinstance(x, float):
            text = str(x)
            if text[len(text)-2: len(text)] == ".0":
                return text[0:len(text)-2]
        if x == True:
            return "true"
        if x == False:
            return "false"
        return str(x)  # rely on object __str__ method
