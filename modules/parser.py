import pickle
import copy
from functools import wraps

from modules.enums import Class


class Node:
    pass


class Program(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


class Var(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class ArrayDecl(Node):
    def __init__(self, id_, type_, start_index, end_index, elems):
        self.id_ = id_
        self.type_ = type_
        self.start_index = start_index
        self.end_index = end_index
        self.elems = elems


class ArrayElem(Node):
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index


class Assign(Node):
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr


class If(Node):
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class Repeat(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class For(Node):
    def __init__(self, start, end, block, type_):
        self.start = start
        self.end = end
        self.block = block
        self.type_ = type_


class Proc(Node):
    def __init__(self, id_, params, variables, block):
        self.id_ = id_
        self.params = params
        self.variables = variables
        self.block = block


class Func(Node):
    def __init__(self, id_, params, type_, variables, block):
        self.id_ = id_
        self.params = params
        self.type_ = type_
        self.variables = variables
        self.block = block


class FuncProcCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Args(Node):
    def __init__(self, args):
        self.args = args


class Params(Node):
    def __init__(self, params):
        self.params = params


class Elems(Node):
    def __init__(self, elems):
        self.elems = elems


class Break(Node):
    pass


class Continue(Node):
    pass


class Exit(Node):
    def __init__(self, return_):
        self.return_ = return_


class Type(Node):
    def __init__(self, value):
        self.value = value


class Int(Node):
    def __init__(self, value):
        self.value = value


class Real(Node):
    def __init__(self, value):
        self.value = value


class Boolean(Node):
    def __init__(self, value):
        self.value = value


class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class ShortString(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second


class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = tokens.pop(0)
        self.prev = None

    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result

        return wrapper

    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0)
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        nodes = []
        while self.curr.class_ == Class.PROCEDURE or self.curr.class_ == Class.FUNCTION:
            if self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.procedure_declaration())
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.function_declaration())
            else:
                self.die_deriv(self.program.__name__)
        if self.curr.class_ == Class.VAR:
            nodes.append(self.variable_declaration_part())
        nodes.append(self.begin_block_end())
        self.eat(Class.DOT)
        return Program(nodes)

    def procedure_declaration(self):
        self.eat(Class.PROCEDURE)
        id_params = self.func_proc_header()
        self.eat(Class.SEMICOLON)
        vars_block = self.func_proc_implementation()
        return Proc(id_params[0], id_params[1], vars_block[0], vars_block[1])

    def function_declaration(self):
        self.eat(Class.FUNCTION)
        id_params = self.func_proc_header()
        self.eat(Class.COLON)
        type_ = self.type_()
        self.eat(Class.SEMICOLON)
        vars_block = self.func_proc_implementation()
        return Func(id_params[0], id_params[1], type_, vars_block[0], vars_block[1])

    def func_proc_header(self):
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        self.eat(Class.LPAREN)
        params = []
        while self.curr.class_ == Class.ID:
            params.extend(self.variable_declaration())
            if self.curr.class_ == Class.SEMICOLON:
                self.eat(Class.SEMICOLON)
        self.eat(Class.RPAREN)
        if len(params) == 0:
            params = None
        else:
            params = Params(params)
        return [id_, params]

    def func_proc_implementation(self):
        vars = None
        if self.curr.class_ == Class.VAR:
            vars = self.variable_declaration_part()
        block = self.begin_block_end()
        self.eat(Class.SEMICOLON)
        return [vars, block]

    def variable_declaration_part(self):
        self.eat(Class.VAR)
        data_type_id = []
        while self.curr.class_ == Class.ID:
            data_type_id.extend(self.variable_declaration())
            self.eat(Class.SEMICOLON)
        return Var(data_type_id)

    def variable_declaration(self):
        data_type_id = []
        ids = []
        ids.append(self.identifier())
        while self.curr.class_ != Class.COLON:
            self.eat(Class.COMMA)
            ids.append(self.identifier())
        self.eat(Class.COLON)
        if self.curr.class_ == Class.ARRAY:
            data_type = self.array_type()
            for id_ in ids:
                data_type.id_ = id_
                data_type_id.append(copy.deepcopy(data_type))
            return data_type_id
        else:
            data_type = self.type_()
            for id_ in ids:
                data_type_id.append(Decl(data_type, id_))
            return data_type_id

    def identifier(self):
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN and self.is_func_proc_call():
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncProcCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET and is_array_elem:
            self.eat(Class.LBRACKET)
            index = self.expression()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            expr = self.is_expression()
            if expr is not False:
                expr = self.logic_expression()
            elif expr is not False:
                expr = None
            return Assign(id_, expr)
        else:
            return id_

    def if_statement(self):
        self.eat(Class.IF)
        cond = self.logic_expression()
        self.eat(Class.THEN)
        true = self.begin_block_end()
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            false = self.begin_block_end()
            self.eat(Class.SEMICOLON)
        else:
            self.eat(Class.SEMICOLON)
        return If(cond, true, false)

    def while_statement(self):
        self.eat(Class.WHILE)
        cond = self.logic_expression()
        self.eat(Class.DO)
        block = self.begin_block_end()
        self.eat(Class.SEMICOLON)
        return While(cond, block)

    def for_statement(self):
        self.eat(Class.FOR)
        start = self.expression()
        if self.curr.class_ == Class.TO:
            self.eat(Class.TO)
            type_ = String("increment")
        elif self.curr.class_ == Class.DOWNTO:
            self.eat(Class.DOWNTO)
            type_ = String("decrement")
        else:
            self.die_deriv(self.for_statement.__name__)
        end = self.expression()
        self.eat(Class.DO)
        block = self.begin_block_end()
        self.eat(Class.SEMICOLON)
        return For(start, end, block, type_)

    def repeat_statement(self):
        self.eat(Class.REPEAT)
        block = self.block()
        self.eat(Class.UNTIL)
        cond = self.logic_expression()
        self.eat(Class.SEMICOLON)
        return Repeat(cond, block)

    def begin_block_end(self):
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        return block

    def block(self):
        nodes = []
        while self.curr.class_ != Class.END and self.curr.class_ != Class.UNTIL:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_statement())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_statement())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_statement())
            elif self.curr.class_ == Class.REPEAT:
                nodes.append(self.repeat_statement())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.EXIT:
                nodes.append(self.exit())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.identifier())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        return Block(nodes)

    def args(self):
        args = []

        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            args.append(self.expression())
            if self.curr.class_ == Class.INT:
                self.eat(Class.INT)
            elif self.curr.class_ == Class.CHAR:
                self.eat(Class.CHAR)
            elif self.curr.class_ == Class.STRING:
                self.eat(Class.STRING)
            elif self.curr.class_ == Class.REAL:
                self.eat(Class.REAL)
            elif self.curr.class_ == Class.BOOLEAN:
                self.eat(Class.REAL)
        return Args(args)

    def exit(self):
        self.eat(Class.EXIT)
        return_ = None
        if self.curr.class_ != Class.SEMICOLON:
            self.eat(Class.LPAREN)
            return_ = self.expression()
            self.eat(Class.RPAREN)
        self.eat(Class.SEMICOLON)
        return Exit(return_)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
        if self.curr.lexeme == "string":
            return self.string_type()
        else:
            return self.simple_type()

    def string_type(self):
        self.eat(Class.TYPE)
        if self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            len = self.curr.lexeme
            self.eat(Class.INT)
            self.eat(Class.RBRACKET)
            return ShortString(len)
        else:
            return Type("string")

    def array_type(self):
        self.eat(Class.ARRAY)
        self.eat(Class.LBRACKET)
        start_index = Int(self.curr.lexeme)
        self.eat(Class.INT)
        self.eat(Class.DOT)
        self.eat(Class.DOT)
        end_index = Int(self.curr.lexeme)
        self.eat(Class.INT)
        self.eat(Class.RBRACKET)
        self.eat(Class.OF)
        type_ = self.simple_type()
        elems = None
        if self.curr.class_ == Class.EQ:
            elems = self.array_element_declaration()
        return ArrayDecl(None, type_, start_index, end_index, elems)

    def array_element_declaration(self):
        self.eat(Class.EQ)
        self.eat(Class.LPAREN)
        elems = []
        elems.append(self.constant())
        while self.curr.class_ == Class.COMMA:
            self.eat(Class.COMMA)
            elems.append(self.constant())
        self.eat(Class.RPAREN)
        return Elems(elems)

    def constant(self):
        if self.curr.class_ == Class.INT:
            value = Int(self.curr.lexeme)
            self.eat(Class.INT)
            return value
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.BOOLEAN:
            value = Boolean(self.curr.lexeme)
            self.eat(Class.BOOLEAN)
            return value
        elif self.curr.class_ == Class.REAL:
            value = Real(self.curr.lexeme)
            self.eat(Class.REAL)
            return value

    def simple_type(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
        if self.curr.class_ in [Class.INT, Class.CHAR, Class.STRING, Class.BOOLEAN, Class.REAL]:
            return self.constant()
        elif self.curr.class_ == Class.ID:
            return self.identifier()
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic_expression()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic_expression()
            self.eat(Class.RPAREN)
            if self.curr.class_ == Class.COLON and type(first) is BinOp:
                self.eat(Class.COLON)
                self.eat(Class.INT)
                self.eat(Class.COLON)
                decimal = Int(self.curr.lexeme)
                self.eat(Class.INT)
                first.decimal = decimal
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.DIV, Class.MOD, Class.FWDSLASH]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.DIV:
                op = self.curr.lexeme
                self.eat(Class.DIV)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MOD:
                op = self.curr.lexeme
                self.eat(Class.MOD)
                second = self.factor()
                first = BinOp(op, first, second)
            if self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
        return first

    def expression(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        first = self.expression()
        if self.curr.class_ == Class.EQ:
            op = self.curr.lexeme
            self.eat(Class.EQ)
            second = self.expression()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expression()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expression()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expression()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expression()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expression()
            return BinOp(op, first, second)
        else:
            return first

    def logic_term(self):
        first = self.compare()
        while self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            first = BinOp(op, first, second)
        while self.curr.class_ == Class.XOR:
            op = self.curr.lexeme
            self.eat(Class.XOR)
            second = self.compare()
            first = BinOp(op, first, second)
        return first

    def logic_expression(self):
        first = self.logic_term()
        while self.curr.class_ == Class.OR:
            op = self.curr.lexeme
            self.eat(Class.OR)
            second = self.logic_term()
            first = BinOp(op, first, second)
        return first

    @restorable
    def is_func_proc_call(self):
        try:
            self.eat(Class.LPAREN)
            self.args()
            self.eat(Class.RPAREN)
            return self.curr.class_ != Class.BEGIN
        except:
            return False

    @restorable
    def is_logic_expression(self):
        try:
            return self.logic_expression()
        except:
            return False

    @restorable
    def is_expression(self):
        try:
            return self.expression()
        except:
            return False

    def parse(self):
        return self.program()

    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))
