import re

from modules.grapher import Visitor
from modules.parser import Program, Var, Block, String, Char, ArrayElem, BinOp, FuncProcCall, If, For, Repeat, While, \
    Func, Proc


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0
        self.symbol_tables = [ast.symbols]

    def get_var_type(self, id_):
        for curr in reversed(self.symbol_tables):
            if curr.contains(id_):
                return curr.get(id_).type_

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
        self.append('''
void insert(char tmp, char* a, int p)
{
    int i=0;
	int t=0;
	int x,g,s,o;
	char c[100], b[100];
	b[0]=tmp;
	b[1]='\0';
	int	r = strlen(a);
	int n = strlen(b);
   	while(i <= r)
	{
		c[i]=a[i];
		i++;
	}
	s = n+r;
	o = p+n;

	for(i=p;i<s;i++)
	{
		x = c[i];
		if(t<n)
		{
			a[i] = b[t];
			t=t+1;
		}
		a[o]=x;
		o=o+1;
	}
}''')
        self.newline()
        self.indent()

    def visit_Program(self, parent, node):
        self.libs()
        is_in_main = True
        for n in node.nodes:
            if is_in_main and (isinstance(n, Var) or isinstance(n, Block)):
                self.append("int main()")
                self.newline()
                self.open_scope()
                is_in_main = False
            self.visit(node, n)
        self.indent()
        self.append("return 0;")
        self.newline()
        self.close_scope()

    def is_control_flow(self, node):
        if isinstance(node, If):
            return True
        if isinstance(node, For):
            return True
        if isinstance(node, Repeat):
            return True
        if isinstance(node, While):
            return True
        return False

    def visit_Block(self, parent, node):
        if not isinstance(parent, Program):
            self.symbol_tables.append(node.symbols)
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            if not self.is_control_flow(n):
                self.append(";")
            self.newline()
        if len(self.symbol_tables) > 1:
            self.symbol_tables.pop()

    def get_format(self, curr_var_type):
        if curr_var_type == 'integer' or  curr_var_type == 'boolean':
            return "d"
        if curr_var_type == 'char':
            return "c"
        if curr_var_type == 'string':
            return "s"
        if curr_var_type == 'real':
            return "f"

    def visit_FuncProcCall(self, parent, node):
        func = node.id_.value
        if func == 'writeln' or func == 'write':
            self.append('printf')
            self.append('(')
            printString = ""
            for arg in node.args.args:
                if isinstance(arg, String) or isinstance(arg, Char):
                    printString += arg.value
                else:
                    if isinstance(arg, ArrayElem):
                        curr_symbol = self.get_var_type(arg.id_.value)
                    elif isinstance(arg, BinOp):
                        curr_symbol = self.get_var_type(arg.first.value)
                    elif isinstance(arg, FuncProcCall):
                        curr_symbol = self.get_var_type(arg.id_.value)
                    else:
                        curr_symbol = self.get_var_type(arg.value)
                    if hasattr(arg, 'decimal'):
                        decimal = arg.decimal.value
                        formatting = "%." + str(decimal) + self.get_format(curr_symbol)
                    else:
                        formatting = "%" + self.get_format(curr_symbol)
                    printString += formatting

            self.append('"')
            self.append(printString)
            if func == 'writeln':
                self.append("\\n")
            self.append('"')
            for arg in node.args.args:
                if not isinstance(arg, String) and not isinstance(arg, Char):
                    self.append(', ')
                    self.visit(node.args, arg)
            self.append(')')
        elif func == 'read' or func == 'readln':
            for i,arg in enumerate(node.args.args):
                self.append('scanf')
                self.append('(')
                self.append('"')
                if isinstance(arg, ArrayElem):
                    curr_symbol = self.get_var_type(arg.id_.value)
                else:
                    curr_symbol = self.get_var_type(arg.value)
                self.append("%")
                self.append(self.get_format(curr_symbol))
                self.append('", ')
                if curr_symbol != "string":
                    self.append("&")
                self.visit(node.args, arg)
                self.append(')')
                if i < len(node.args.args) - 1:
                    self.append("; ")
                    self.newline()
                    self.indent()
        elif func == 'ord' or func == 'chr':
            self.visit(node, node.args)
        elif func == 'length':
            self.append("strlen(")
            self.visit(node, node.args)
            self.append(")")
        elif func == 'inc':
            self.visit(node, node.args)
            self.append("++")
        else:
            self.append(func)
            self.append('(')
            self.visit(node, node.args)
            self.append(')')

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

    def visit_Continue(self, parent, node):
        self.append("continue")

    def visit_Break(self, parent, node):
        self.append("break")

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
        elif node.symbol == '<>':
            self.append(" != ")
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
        self.visit(node, node.type_)
        self.append(" ")
        self.visit(node, node.id_)
        if node.type_.value == 'string':
            self.append("[100]")


    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append(" = ")
        self.visit(node, node.expr)

    def visit_Type(self, parent, node):
        if node.value == 'integer' or node.value =='boolean':
            self.append('int')
        elif node.value == 'real':
            self.append('float')
        elif node.value == 'string':
            self.append('char')
        else:
            self.append(node.value)

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_For(self, parent, node):
        self.append("for")
        self.append("(")
        self.visit(node, node.start)
        self.append("; ")
        self.visit(node.start, node.start.id_)
        if node.type_.value == "increment":
            self.append(" <= ")
        elif node.type_.value == "decrement":
            self.append(" >= ")
        self.visit(node, node.end)
        self.append("; ")
        self.visit(node.start, node.start.id_)
        if node.type_.value == "increment":
            self.append("++")
        elif node.type_.value == "decrement":
            self.append("--")
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
        self.append("return")
        if node.return_ is not None:
            self.append("(")
            self.visit(node, node.return_)
            self.append(")")

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node, node.index)
        self.append(']')

    def visit_ArrayDecl(self, parent, node):
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

    def visit_UnOp(self, parent, node):
        self.append(node.symbol)
        self.visit(node, node.first)

    def visit_Repeat(self, parent, node):
        self.append("do")
        self.open_scope()
        self.visit(node, node.block)
        self.close_scope()
        self.indent()
        self.append("while(!(")
        self.visit(node, node.cond)
        self.append("));")

    def visit_While(self, parent, node):
        self.append("while(")
        self.visit(node, node.cond)
        self.append(")")
        self.open_scope()
        self.visit(node, node.block)
        self.close_scope()

    def visit_Boolean(self, parent, node):
        if node.value == 'true':
            self.append("1")
        elif node.value == 'false':
            self.append("0")

    def generate(self, path):
        self.visit(None, self.ast)
        self.py = re.sub('\n\s*\n', '\n', self.py)
        with open(path, 'w') as source:
            source.write(self.py)
        return path
