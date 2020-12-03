import re

from modules.grapher import Visitor
from modules.parser import Program, Var, Block, String


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0

    def append(self, text):
        self.py += str(text)

    def newline(self):
        self.append('\n')

    def indent(self):
        for i in range(self.level):
            self.append('\t')

    def open_scope(self):
        self.indent()
        self.append("{")
        self.newline()
        self.level += 1

    def close_scope(self):
        self.level -= 1
        self.indent()
        self.append("}")
        self.newline()

    def libs(self):
        self.append("#include<stdio.h>")
        self.newline()

    def visit_Program(self, parent, node):
        self.libs()
        is_in_main = True
        for n in node.nodes:
            if is_in_main and (type(n) is Var or type(n) is Block):
                self.append("int main()")
                self.newline()
                self.open_scope()
                is_in_main = False
            self.visit(node, n)
        self.indent()
        self.append("return 0;")
        self.newline()
        self.close_scope()

    def visit_Block(self, parent, node):
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.newline()

    def visit_FuncProcCall(self, parent, node):
        func = node.id_.value
        if func == 'writeln' or func == 'write':
            self.append('printf')
            self.append('(')
            printString = ""
            for arg in node.args.args:
                if type(arg) is String:
                    printString += arg.value
                else:
                    printString += " %d "
            self.append('"')
            self.append(printString)
            if func == 'writeln':
                self.append("\\n")
            self.append('"')
            for i, arg in enumerate(node.args.args):
                if type(arg) is not String:
                    if i > 0:
                        self.append(', ')
                    self.visit(node.args, arg)
        elif func == 'read' or func == 'readln':
            self.append('scanf')
            self.append('(')
            self.append('"%d", &')
            self.visit(node, node.args)
        else:
            self.append(func)
            self.append('(')
        self.append(')')
        self.append("; ")

    def visit_Args(self, parent, node):
        for i, a in enumerate(node.args):
            if i > 0:
                self.append(', ')
            self.visit(node, a)

    def visit_String(self, parent, node):
        self.append('"')
        self.append(node.value)
        self.append('"')

    def visit_Char(self, parent, node):
        self.append("'")
        self.append(node.value)
        self.append("'")

    def visit_Int(self, parent, node):
        self.append(node.value)

    def visit_BinOp(self, parent, node):
        self.visit(node, node.first)
        if node.symbol == '=':
            self.append(' ' + '==' + ' ')
        else:
            self.append(' ' + node.symbol + ' ')
        self.visit(node, node.second)

    def visit_Var(self, parent, node):
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        self.indent()
        self.visit(node, node.type_)
        self.append(" ")
        self.visit(node, node.id_)
        self.append(";")
        self.newline()

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append(" = ")
        self.visit(node, node.expr)
        self.append("; ")

    def visit_Type(self, parent, node):
        if node.value == "integer":
            self.append("int")
        else:
            self.append(node.value)

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_For(self, parent, node):
        self.append("for")
        self.append("(")
        self.visit(node, node.start)
        self.visit(node.start, node.start.id_)
        self.append(" <= ")
        self.visit(node, node.end)
        self.append("; ")
        self.visit(node.start, node.start.id_)
        self.append("++")
        self.append(")")
        self.newline()
        self.open_scope()
        self.visit(node, node.block)
        self.close_scope()

    def visit_If(self, parent, node):
        self.append("if( ")
        self.visit(node, node.cond)
        self.append(" )")
        self.newline()
        self.open_scope()
        self.visit(node, node.true)
        self.close_scope()
        if node.false is not None:
            self.indent()
            self.append('else')
            self.newline()
            self.open_scope()
            self.visit(node, node.false)
            self.close_scope()

    def generate(self, path):
        self.visit(None, self.ast)
        self.py = re.sub('\n\s*\n', '\n', self.py)
        with open(path, 'w') as source:
            source.write(self.py)
        return path
