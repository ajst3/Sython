"""
Script that generates the expression classes.
"""
import sys


class ExpGen(object):

    def __init__(self, outputdir):
        self.outputdir = outputdir
        self.basename = "expressions"

        # Maps the fields for the type of expression to the type of expression
        self.exp_map = {
        "Binary": "left, operator, right",
        "Grouping": "expression",
        "Literal": "val",
        "Unary": "operator, right"
        }
        self.path_to_file = ("%s/%s.py" % (self.outputdir, self.basename))
        self.expfile = open("%s" % self.path_to_file, 'w')

    def _setupFile(self):
        file_preamble = ("# File that hols the classes for the various"
                         " the expressions\n")
        self.expfile.write(file_preamble)

        # Write the base class shared by all
        base_class = ("class Expression():\n\tpass\n\n")
        self.expfile.write(base_class)

    def _addClass(self, classname):
        class_sign = "class %s(Expression):\n\t" % classname
        self.expfile.write(class_sign)

        class_params = self.exp_map[classname]
        init = ("def __init__(self, %s):\n" % class_params)
        self.expfile.write(init)

        class_params = class_params.split(',')
        for param in class_params:
            param = param.strip()
            field_def = "\t\tself.%s = %s\n" % (param, param)
            self.expfile.write(field_def)


    def designAst(self):
        # Add the file preamble and the base class
        self._setupFile()

        # Add each class to file
        for classname in self.exp_map:
            self._addClass(classname)
            self.expfile.write("\n")

    def tear_down(self):
        self.expfile.close()


if __name__ == "__main__":
    gen = ExpGen(sys.argv[1].strip('"'))
    gen.designAst()
