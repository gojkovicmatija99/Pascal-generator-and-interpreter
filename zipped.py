from enum import Enum, auto


class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DIV = auto()
    MOD = auto()
    FWDSLASH = auto()

    OR = auto()
    AND = auto()
    NOT = auto()
    XOR = auto()

    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()

    ASSIGN = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()

    TYPE = auto()
    INT = auto()
    REAL = auto()
    CHAR = auto()
    BOOLEAN = auto()
    STRING = auto()
    ARRAY = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    REPEAT = auto()
    UNTIL = auto()
    BEGIN = auto()
    END = auto()
    VAR = auto()
    PROCEDURE = auto()
    FUNCTION = auto()
    TO = auto()
    DOWNTO = auto()
    DO = auto()
    THEN = auto()
    OF = auto()

    BREAK = auto()
    CONTINUE = auto()
    EXIT = auto()

    ID = auto()

    DOT = auto()
    EOF = auto()


class Token:
    def __init__(self, class_, lexeme):
        self.class_ = class_
        self.lexeme = lexeme

    def __str__(self):
        return "<{} {}>".format(self.class_, self.lexeme)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.len = len(text)
        self.pos = -1

    def read_space(self):
        while self.pos + 1 < self.len and self.text[self.pos + 1].isspace():
            self.next_char()

    def read_int(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.next_char()
        return int(lexeme)

    def read_char(self):
        self.pos += 1
        lexeme = self.text[self.pos]
        self.pos += 1
        return lexeme

    def read_string(self):
        lexeme = ''
        while self.pos + 1 < self.len and self.text[self.pos + 1] != '\'':
            lexeme += self.next_char()
        self.pos += 1
        return lexeme

    def is_only_one_char(self):
        if self.text[self.pos + 2] == '\'':
            return True
        return False

    def read_keyword(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and (self.text[self.pos + 1].isalnum() or self.text[self.pos + 1] == '_'):
            lexeme += self.next_char()
        if lexeme == 'if':
            return Token(Class.IF, lexeme)
        elif lexeme == 'else':
            return Token(Class.ELSE, lexeme)
        elif lexeme == 'while':
            return Token(Class.WHILE, lexeme)
        elif lexeme == 'for':
            return Token(Class.FOR, lexeme)
        elif lexeme == 'repeat':
            return Token(Class.REPEAT, lexeme)
        elif lexeme == 'until':
            return Token(Class.UNTIL, lexeme)
        elif lexeme == 'break':
            return Token(Class.BREAK, lexeme)
        elif lexeme == 'continue':
            return Token(Class.CONTINUE, lexeme)
        elif lexeme == 'exit':
            return Token(Class.EXIT, lexeme)
        elif lexeme == 'var':
            return Token(Class.VAR, lexeme)
        elif lexeme == 'begin':
            return Token(Class.BEGIN, lexeme)
        elif lexeme == 'end':
            return Token(Class.END, lexeme)
        elif lexeme == 'array':
            return Token(Class.ARRAY, lexeme)
        elif lexeme == 'procedure':
            return Token(Class.PROCEDURE, lexeme)
        elif lexeme == 'function':
            return Token(Class.FUNCTION, lexeme)
        elif lexeme == 'to':
            return Token(Class.TO, lexeme)
        elif lexeme == 'downto':
            return Token(Class.DOWNTO, lexeme)
        elif lexeme == 'do':
            return Token(Class.DO, lexeme)
        elif lexeme == 'div':
            return Token(Class.DIV, lexeme)
        elif lexeme == 'mod':
            return Token(Class.MOD, lexeme)
        elif lexeme == 'then':
            return Token(Class.THEN, lexeme)
        elif lexeme == 'of':
            return Token(Class.OF, lexeme)
        elif lexeme == 'and':
            return Token(Class.AND, lexeme)
        elif lexeme == 'or':
            return Token(Class.OR, lexeme)
        elif lexeme == 'not':
            return Token(Class.NOT, lexeme)
        elif lexeme == 'xor':
            return Token(Class.XOR, lexeme)
        elif lexeme == 'true':
            return Token(Class.BOOLEAN, lexeme)
        elif lexeme == 'false':
            return Token(Class.BOOLEAN, lexeme)
        elif lexeme == 'integer' or lexeme == 'char' or lexeme == 'string' or lexeme == 'real' or lexeme == 'boolean':
            return Token(Class.TYPE, lexeme)
        return Token(Class.ID, lexeme)

    def next_char(self):
        self.pos += 1
        if self.pos >= self.len:
            return None
        return self.text[self.pos]

    def next_token(self):
        self.read_space()
        curr = self.next_char()
        if curr is None:
            return Token(Class.EOF, curr)
        token = None
        if curr.isalpha():
            token = self.read_keyword()
        elif curr.isdigit():
          firstInt = self.read_int()
          curr = self.next_char()
          if curr == '.':
            curr = self.next_char()
            if curr.isdigit():
                secondInt = self.read_int()
                token = Token(Class.REAL, f'{firstInt}.{secondInt}')
            else:
                self.pos -= 2
                token = Token(Class.INT, firstInt)
          else:
            self.pos -= 1
            token = Token(Class.INT, firstInt)
        elif curr == '\'':
            if self.is_only_one_char():
                token = Token(Class.CHAR, self.read_char())
            else:
                token = Token(Class.STRING, self.read_string())
        elif curr == '+':
            token = Token(Class.PLUS, curr)
        elif curr == '-':
            token = Token(Class.MINUS, curr)
        elif curr == '*':
            token = Token(Class.STAR, curr)
        elif curr == '/':
            token = Token(Class.FWDSLASH, curr)
        elif curr == '.':
            token = Token(Class.DOT, curr)
        elif curr == '=':
            token = Token(Class.EQ, '=')
        elif curr == ':':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.ASSIGN, ':=')
            else:
                token = Token(Class.COLON, ':')
                self.pos -= 1
        elif curr == '<':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.LTE, '<=')
            elif curr == '>':
                token = Token(Class.NEQ, '<>')
            else:
                token = Token(Class.LT, '<')
                self.pos -= 1
        elif curr == '>':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.GTE, '>=')
            else:
                token = Token(Class.GT, '>')
                self.pos -= 1
        elif curr == '(':
            token = Token(Class.LPAREN, curr)
        elif curr == ')':
            token = Token(Class.RPAREN, curr)
        elif curr == '[':
            token = Token(Class.LBRACKET, curr)
        elif curr == ']':
            token = Token(Class.RBRACKET, curr)
        elif curr == ';':
            token = Token(Class.SEMICOLON, curr)
        elif curr == ',':
            token = Token(Class.COMMA, curr)
        else:
            self.die(curr)
        return token

    def lex(self):
        tokens = []
        while True:
            curr = self.next_token()
            tokens.append(curr)
            if curr.class_ == Class.EOF:
                break
        return tokens

    def die(self, char):
        print(self.pos)
        raise SystemExit("Unexpected character: {}".format(char))

import pickle
import copy
from functools import wraps

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
            type_ = String("increase")
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

class Visitor():
    def visit(self, parent, node):
        method = 'visit_' + type(node).__name__
        visitor = getattr(self, method, self.die)
        return visitor(parent, node)

    def die(self, parent, node):
        method = 'visit_' + type(node).__name__
        raise SystemExit("Missing method: {}".format(method))

class Symbol:
    def __init__(self, id_, type_, scope):
        self.id_ = id_
        self.type_ = type_
        self.scope = scope

    def __str__(self):
        return "<{} {} {}>".format(self.id_, self.type_, self.scope)

    def copy(self):
        return Symbol(self.id_, self.type_, self.scope)


class Symbols:
    def __init__(self):
        self.symbols = {}

    def put(self, id_, type_, scope):
        self.symbols[id_] = Symbol(id_, type_, scope)

    def get(self, id_):
        return self.symbols[id_]

    def contains(self, id_):
        return id_ in self.symbols

    def remove(self, id_):
        del self.symbols[id_]

    def __len__(self):
        return len(self.symbols)

    def __str__(self):
        out = ""
        for _, value in self.symbols.items():
            if len(out) > 0:
                out += "\n"
            out += str(value)
        return out

    def __iter__(self):
        return iter(self.symbols.values())

    def __next__(self):
        return next(self.symbols.values())


class Symbolizer(Visitor):
    def __init__(self, ast):
        self.ast = ast

    # some predefined functions
    def symbolize_libs(self, node):
        node.symbols.put('chr', 'char', id(node))

    def visit_Program(self, parent, node):
        node.symbols = Symbols()
        self.symbolize_libs(node)
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))

    def visit_ArrayDecl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))

    def visit_ArrayElem(self, parent, node):
        pass

    def visit_Assign(self, parent, node):
        pass

    def visit_If(self, parent, node):
        self.visit(node, node.true)
        if node.false is not None:
            self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.visit(node, node.block)

    def visit_For(self, parent, node):
        self.visit(node, node.block)

    def visit_Repeat(self, parent, node):
        self.visit(node, node.block)

    def visit_Proc(self, parent, node):
        parent.symbols.put(node.id_.value, "void", id(parent))
        self.visit(node, node.block)
        self.visit(node, node.params)

    def visit_Func(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))
        self.visit(node, node.block)
        self.visit(node, node.params)

    def visit_FuncProcCall(self, parent, node):
        pass

    def visit_Block(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Params(self, parent, node):
        node.symbols = Symbols()
        for p in node.params:
            self.visit(node, p)
            self.visit(parent.block, p)

    def visit_Var(self, parent, node):
        for n in node.nodes:
            self.visit(parent, n)

    def visit_Args(self, parent, node):
        pass

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
        pass

    def visit_Char(self, parent, node):
        pass

    def visit_String(self, parent, node):
        pass

    def visit_Boolean(self, parent, node):
        pass

    def visit_Real(self, parent, node):
        pass

    def visit_Id(self, parent, node):
        pass

    def visit_BinOp(self, parent, node):
        pass

    def visit_UnOp(self, parent, node):
        pass

    def symbolize(self):
        self.visit(None, self.ast)

import re


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
        if node.type_.value == "increase":
            self.append(" <= ")
        elif node.type_.value == "decrement":
            self.append(" >= ")
        self.visit(node, node.end)
        self.append("; ")
        self.visit(node.start, node.start.id_)
        if node.type_.value == "increase":
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

import re
from _ast import Return
import numpy as np

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
            value = value.value
        id_.value = value

    def visit_If(self, parent, node):
        cond = self.visit(node, node.cond)
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
            self.visit(node, node.args)
            result = self.visit(node, impl.block)
            self.clear_scope(impl.block)
            self.return_ = False
            return result

    def visit_Block(self, parent, node):
        result = None
        scope = id(node)
        self.scope.append(scope)
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
            arg = self.visit(impl.block, a)
            id_ = self.visit(impl.block, p.id_)
            id_.value = arg
            if isinstance(arg, Symbol):
                id_.value = arg.value

    def visit_Elems(self, parent, node):
        pass

    def visit_Break(self, parent, node):
        pass

    def visit_Continue(self, parent, node):
        pass

    def visit_Return(self, parent, node):
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
        elif node.symbol == '==':
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
            bool_first = first != 0
            return not bool_first
        elif node.symbol == '&':
            return backup_first
        else:
            return None

    def run(self):
        self.visit(None, self.ast)

import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('src')  # Izvorna PAS datoteka
arg_parser.add_argument('gen')  # Generisana C datoteka
args = vars(arg_parser.parse_args())

with open(args['src'], 'r') as source:
    text = source.read()
    lexer = Lexer(text)
    tokens = lexer.lex()
    parser = Parser(tokens)
    ast = parser.parse()
    symbolizer = Symbolizer(ast)
    symbolizer.symbolize()
    generator = Generator(ast)
    generator.generate(args['gen'])
    runner = Runner(ast)
    runner.run()