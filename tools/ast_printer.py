"""
Used for debugging. Can print out an expression neatly.
"""

class Printer(object):

    def printExp(self, exp):
        return exp.accept(self)

    def _parens(self, op, *exps):
        to_return = "(%s" % op
        #print(to_return)
        for exp in exps:
            to_return += ' '
            to_return += exp.accept(self)
        to_return += ')'
        return to_return

    def visitBinary(self, binexp):
        return self._parens(binexp.operator.lexeme, binexp.left, binexp.right)

    def visitGrouping(self, groupexp):
        return self._parens("group", groupexp.expression)

    def visitLiteral(self, litexp):
        if litexp.val == 'nil':
            return None
        return str(litexp.val)

    def visitUnary(self, unexp):
        return self._parens(unexp.operator.lexeme, unexp.right)
