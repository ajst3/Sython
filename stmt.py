# This file was generated by the expresion_generator tool.
# Holds all of the expression classes.

class Stmt():
	def accept(self, visitor):
		pass

class Expression(Stmt):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitExpression(self)

class Print(Stmt):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitPrint(self)

class Var(Stmt):
	def __init__(self, name, initializer):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor):
		return visitor.visitVar(self)
