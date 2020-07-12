"""
Script that generates the expression classes.
"""
import sys


class ExpGen(object):

    def __init__(self, outputdir, filename, basename):
        self.outputdir = outputdir
        self.basename = basename
        self.filename = filename

        # Maps the fields for the type of expression to the type of expression
        self.exp_map = {
        "Assign": "name, value",
        "Binary": "left, operator, right",
        "Logical": "left, operator, right",
        "Grouping": "expression",
        "Literal": "val",
        "Unary": "operator, right",
        "Variable": "name"
        }
        self.stmt_map = {
        "If": "condition, then_branch, else_branch",
        "Block": "statements",
        "Expression": "expression",
        "Print": "expression",
        "Var": "name, type, initializer",
        "While": "condition, body",
        "For": "initializer, condition, body, increment, else_branch",
        "Do": "condition, body, condition_type",
        "Until": "condition, body"
        }
        self.path_to_file = ("%s/%s.py" % (self.outputdir, self.filename))
        self.expfile = open("%s" % self.path_to_file, 'w')

    def _setupFile(self):
        file_preamble = ("# This file was generated by the expresion_"
                         "generator tool.\n# Holds all of the expression"
                         " classes.\n\n")
        self.expfile.write(file_preamble)

        # Write the base class shared by all
        base_class = ("class %s():\n" % self.basename)
        self.expfile.write(base_class)

        # Add abstract method to the base class
        abstract_vis = ("\tdef accept(self, visitor):\n\t\tpass\n\n")
        self.expfile.write(abstract_vis)

    def _addVisitor(self, types, basename):
        class_sign = ("class Visitor(object):\n\t")
        self.expfile.write(class_sign)

        for typename in types:
            method_sig = ("def visit%s%s(%s):\n" % (typename, basename,
                                                 basename.lower()))
            self.expfile.write(method_sig)
            self.expfile.write("\t\tpass\n")

    def _addClass(self, classname, map):
        class_sign = ("class %s(%s):\n\t" % (classname, self.basename))
        self.expfile.write(class_sign)

        # Add constructor
        class_params = map[classname]
        init = ("def __init__(self, %s):\n" % class_params)
        self.expfile.write(init)

        # Add field definitions to constructor
        class_params = class_params.split(',')
        for param in class_params:
            param = param.strip()
            field_def = "\t\tself.%s = %s\n" % (param, param)
            self.expfile.write(field_def)

        # Add accept method
        accept_sig = ("\n\tdef accept(self, visitor):\n")
        accept_body = ("\t\treturn visitor.visit%s(self)\n" % classname)
        self.expfile.write(accept_sig)
        self.expfile.write(accept_body)

    def designAst(self):
        # Add the file preamble and the base class
        self._setupFile()

        # Add each class to file
        if self.basename == "Expression":
            map = self.exp_map
        elif self.basename == "Stmt":
            map = self.stmt_map

        for classname in map:
            self._addClass(classname, map)
            self.expfile.write("\n")


    def tear_down(self):
        self.expfile.close()


if __name__ == "__main__":
    gen = ExpGen(sys.argv[1].strip('"'), sys.argv[2], sys.argv[3])
    gen.designAst()
    gen.tear_down()
