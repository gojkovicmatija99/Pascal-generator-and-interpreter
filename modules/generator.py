import re

from modules.grapher import Visitor
from modules.parser import Program, Var, Block, String, Char, ArrayElem


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0
        self.var_type = {}

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

    def get_format(self, curr_var_type):
        if curr_var_type == 'integer':
            return "%d"
        if curr_var_type == 'char':
            return "%c"
        if curr_var_type == 'string':
            return "%s"
        if curr_var_type == 'real':
            return "%f"

    def visit_FuncProcCall(self, parent, node):
        func = node.id_.value
        if func == 'writeln' or func == 'write':
            self.append('printf')
            self.append('(')
            printString = ""
            for arg in node.args.args:
                if type(arg) is String or type(arg) is Char:
                    printString += arg.value
                else:
                    if type(arg) is ArrayElem:
                        curr_var_type = self.var_type[arg.id_.value]
                    else:
                        curr_var_type = self.var_type[arg.value]
                    printString += self.get_format(curr_var_type)

            self.append('"')
            self.append(printString)
            if func == 'writeln':
                self.append("\\n")
            self.append('"')
            for arg in node.args.args:
                if type(arg) is not String and type(arg) is not Char:
                    self.append(', ')
                    self.visit(node.args, arg)
            self.append(')')
            self.append("; ")
        elif func == 'read' or func == 'readln':
            for arg in node.args.args:
                self.append('scanf')
                self.append('(')
                self.append('"')
                if type(arg) is ArrayElem:
                    curr_var_type = self.var_type[arg.id_.value]
                else:
                    curr_var_type = self.var_type[arg.value]
                self.append(self.get_format(curr_var_type))
                self.append('", &')
                self.visit(node.args, arg)
                self.append(')')
                self.append("; ")
                self.newline()
                self.indent()
        else:
            self.append(func)
            self.append('(')
            self.visit(node, node.args)
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
        elif node.symbol == 'mod':
            self.append(" % ")
        elif node.symbol == 'div':
            self.append(" / ")
        elif node.symbol == 'and':
            self.append(" && ")
        elif node.symbol == 'or':
            self.append(" || ")
        else:
            self.append(' ' + node.symbol + ' ')
        self.visit(node, node.second)

    def visit_Var(self, parent, node):
        for n in node.nodes:
            self.newline()
            self.indent()
            self.visit(node, n)
            self.append(";")
        self.newline()

    def visit_Decl(self, parent, node):
        self.var_type[node.id_.value] = node.type_.value
        self.visit(node, node.type_)
        self.append(" ")
        self.visit(node, node.id_)


    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append(" = ")
        self.visit(node, node.expr)
        self.append("; ")

    def visit_Type(self, parent, node):
        if node.value == "integer":
            self.append("int")
        elif node.value == "real":
            self.append("float")
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
        self.append("if(")
        self.visit(node, node.cond)
        self.append(")")
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

    def visit_Proc(self, parent, node):
        self.append("void ")
        self.visit(node, node.id_)
        self.append("(")
        if node.params is not None:
            for i, param in enumerate(node.params.params):
                if i > 0:
                    self.append(", ")
                self.visit(node.params, param)
        self.append(")")
        self.newline()
        self.open_scope()
        if node.variables is not None:
            self.visit(node, node.variables)
        self.visit(node, node.block)
        self.close_scope()

    def visit_Func(self, parent, node):
        self.visit(node, node.type_)
        self.append(" ")
        self.visit(node, node.id_)
        self.append("(")
        if node.params is not None:
            for i, param in enumerate(node.params.params):
                if i > 0:
                    self.append(", ")
                self.visit(node.params, param)
        self.append(")")
        self.newline()
        self.open_scope()
        if node.variables is not None:
            self.visit(node, node.variables)
        self.indent()
        self.visit(node, node.type_)
        self.append(" ")
        self.visit(node, node.id_)
        self.append(";")
        self.newline()
        self.visit(node, node.block)
        self.indent()
        self.append("return ")
        self.visit(node, node.id_)
        self.append(";")
        self.newline()
        self.close_scope()

    def visit_Params(self, parent, node):
        for i, p in enumerate(node.params):
            if i > 0:
                self.append(', ')
            self.visit(p, p.type_)
            self.append(" ")
            self.visit(p, p.id_)

    def visit_Exit(self, parent, node):
        self.append("return;")

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node, node.index)
        self.append(']')

    def visit_ArrayDecl(self, parent, node):
        self.var_type[node.id_.value] = node.type_.value
        self.visit(node, node.type_)
        self.append(" ")
        self.visit(node, node.id_)
        self.append("[")
        maxElems = node.end_index.value - node.start_index.value + 1
        self.append(str(maxElems))
        self.append("]")
        if node.elems is not None:
            self.visit(node, node.elems)

    def visit_Elems(self, parent, node):
        self.append(" = {")
        for i, elem in enumerate(node.elems):
            if i > 0:
                self.append(", ")
            self.visit(node, elem)
        self.append("}")

    def generate(self, path):
        self.visit(None, self.ast)
        self.py = re.sub('\n\s*\n', '\n', self.py)
        with open(path, 'w') as source:
            source.write(self.py)
        return path
