import re
from _ast import Return
import numpy as np

from modules.grapher import Visitor
from modules.parser import Int, Char, String, Id, Continue, Break, BinOp, FuncProcCall
from modules.symbolizer import Symbol


class Runner(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_ = {}
        self.local = {}
        self.scope = []
        self.return_ = False

    def get_symbol(self, node):
        id_ = node.value
        for scope in reversed(self.scope):
            if scope in self.local:
                curr_scope = self.local[scope][-1]
                if id_ in curr_scope:
                    return curr_scope[id_]
        return self.global_[id_]

    def init_scope(self, node):
        scope = id(node)
        if scope not in self.local:
            self.local[scope] = []
        self.local[scope].append({})
        for s in node.symbols:
            self.local[scope][-1][s.id_] = s.copy()

    def clear_scope(self, node):
        scope = id(node)
        self.local[scope].pop()

    def visit_Program(self, parent, node):
        for s in node.symbols:
            self.global_[s.id_] = s.copy()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Var(self, parent, node):
        for decl in node.nodes:
            self.visit(node, decl)

    def visit_Decl(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.value = None

    def visit_ArrayDecl(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.symbols = node.symbols
        start = self.visit(node, node.start_index)
        end = self.visit(node, node.end_index)
        size = end - start + 1
        # size, elems = node.size, node.elems
        # if elems is not None:
        #     self.visit(node, elems)
        for i in range(size):
            id_.symbols.put(i, id_.type_, None)
            id_.symbols.get(i).value = None

    def visit_ArrayElem(self, parent, node):
        if isinstance(node.index, Id):
            index = self.get_symbol(node.index).value
        else:
            index = node.index.value
        return (node.id_, index)

    def visit_Assign(self, parent, node):
        id_ = self.visit(node, node.id_)
        value = self.visit(node, node.expr)
        if isinstance(value, Symbol):
            id_.value = value.value
        id_.value = value

    def visit_If(self, parent, node):
        cond = self.visit(node, node.cond)
        if isinstance(cond, Symbol):
            cond = cond.value
        if cond:
            self.init_scope(node.true)
            self.visit(node, node.true)
            self.clear_scope(node.true)
        else:
            if node.false is not None:
                self.init_scope(node.false)
                self.visit(node, node.false)
                self.clear_scope(node.false)

    def visit_While(self, parent, node):
        cond = self.visit(node, node.cond)
        while cond:
            self.init_scope(node.block)
            self.visit(node, node.block)
            self.clear_scope(node.block)
            cond = self.visit(node, node.cond)

    def check_condition(self, first, second, type_):
        val_first = self.get_symbol(first).value
        if isinstance(second, Id):
            val_second = self.get_symbol(second).value
        else:
            val_second = second.value
        if type_ == 'increase':
            cond = val_first < val_second
        else:
            cond = val_first >= val_second
        return cond

    def visit_For(self, parent, node):
        self.visit(node, node.start)
        first = node.start.id_
        second = node.end
        type_ = self.visit(node, node.type_)
        cond = self.check_condition(first, second, type_)
        while cond:
            self.init_scope(node.block)
            self.visit(node, node.block)
            self.clear_scope(node.block)
            if type_ == 'increment':
                self.get_symbol(first).value += 1
            else:
                self.get_symbol(first).value -= 1
            cond = self.check_condition(first, second, type_)

    def visit_Func(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.params = node.params
        id_.block = node.block

    def visit_Proc(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.params = node.params
        id_.block = node.block

    def my_ord(self, node, arg):
        if isinstance(arg, Id):
            symb = self.get_symbol(arg)
            val = symb.value
        else:
            val = self.visit(node, arg)
        return ord(val)

    def my_chr(self, node, arg):
        if isinstance(arg, Id):
            symb = self.get_symbol(arg)
            char = symb.value
        else:
            char = self.visit(node, arg)
        return chr(char)

    def isfloat(self, x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def isint(self, x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b

    def visit_FuncProcCall(self, parent, node):
        func = node.id_.value
        args = node.args.args
        if func == 'write' or func == 'writeln':
            format_ = ""
            for arg in args:
                curr = self.visit(node, arg)
                if isinstance(arg, String) or isinstance(arg, Char):
                    format_ += curr
                elif isinstance(arg, BinOp) and hasattr(arg, 'decimal'):
                    format_ += "{:.2f}".format(curr)
                elif isinstance(curr, Symbol):
                    format_ += str(curr.value)
                else:
                    format_ += str(curr)
            if func == 'writeln':
                print(format_)
            else:
                print(format_, end='')
        elif func == 'read' or func == 'readln':
            scan = input()
            vals = scan.split()
            for i, val in enumerate(vals):
                if self.isint(val):
                    scan = int(val)
                elif self.isfloat(val):
                    scan = float(val)
                else:
                    scan = val
                id_ = self.visit(node.args, args[i])
                if id_.type_ == 'integer':
                    id_.value = int(scan)
                elif id_.type_ == 'real':
                    id_.value = float(scan)
                else:
                    id_.value = scan
        elif func == 'ord':
            return self.my_ord(node, args[0])
        elif func == 'chr':
            return self.my_chr(node, args[0])
        else:
            impl = self.global_[func]
            self.init_scope(impl.block)
            result = self.visit(node, impl.block)
            self.clear_scope(impl.block)
            self.return_ = False
            return result

    def visit_Block(self, parent, node):
        result = None
        scope = id(node)
        self.scope.append(scope)
        if isinstance(parent, FuncProcCall):
            self.visit(parent, parent.args)
        for n in node.nodes:
            if self.return_:
                break
            if isinstance(n, Break):
                break
            elif isinstance(n, Continue):
                continue
            elif isinstance(n, Return):
                self.return_ = True
                if n.expr is not None:
                    result = self.visit(n, n.expr)
            else:
                self.visit(node, n)
        self.scope.pop()
        return result

    def visit_Params(self, parent, node):
        pass

    def visit_Args(self, parent, node):
        func = parent.id_.value
        impl = self.global_[func]
        for p, a in zip(impl.params.params, node.args):
            curr_arg = self.visit(impl.block, a)
            arg = self.global_[curr_arg.id_]
            id_ = self.visit(impl.block, p.id_)
            id_.value = arg.value
            # if isinstance(arg, Symbol):
            #     id_.value = arg.value


    def visit_Elems(self, parent, node):
        pass

    def visit_Break(self, parent, node):
        pass

    def visit_Continue(self, parent, node):
        pass

    def visit_Exit(self, parent, node):
        pass

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        return node.value

    def visit_Char(self, parent, node):
        return node.value

    def visit_String(self, parent, node):
        return node.value

    def visit_Id(self, parent, node):
        return self.get_symbol(node)

    def cast(self, symb):
        if isinstance(symb, Symbol):
            num = symb.value
            if symb.type_ == 'integer':
                return int(num)
            elif symb.type_ == 'real':
                return float(num)
            else:
                return num
        else:
            return symb

    def visit_BinOp(self, parent, node):
        first = self.visit(node, node.first)
        second = self.visit(node, node.second)
        if isinstance(first, Symbol):
            first = first.value
            if isinstance(second, Symbol):
                first = second.value
        if node.symbol == '+':
            return self.cast(first) + self.cast(second)
        elif node.symbol == '-':
            return self.cast(first) - self.cast(second)
        elif node.symbol == '*':
            return self.cast(first) * self.cast(second)
        elif node.symbol == 'div':
            return self.cast(first) // self.cast(second)
        elif node.symbol == '/':
            return self.cast(first) / self.cast(second)
        elif node.symbol == 'mod':
            return self.cast(first) % self.cast(second)
        elif node.symbol == '=':
            return first == second
        elif node.symbol == '!=':
            return first != second
        elif node.symbol == '<':
            return self.cast(first) < self.cast(second)
        elif node.symbol == '>':
            return self.cast(first) > self.cast(second)
        elif node.symbol == '<=':
            return self.cast(first) <= self.cast(second)
        elif node.symbol == '>=':
            return self.cast(first) >= self.cast(second)
        elif node.symbol == 'and':
            return self.cast(first) and self.cast(second)
        elif node.symbol == 'or':
            return self.cast(first) or self.cast(second)
        else:
            return None

    def visit_UnOp(self, parent, node):
        first = self.visit(node, node.first)
        backup_first = first
        if isinstance(first, Symbol):
            first = first.value
        if node.symbol == '-':
            return -first
        elif node.symbol == '!':
            bool_first = first != False
            return not bool_first
        else:
            return None

    def run(self):
        self.visit(None, self.ast)