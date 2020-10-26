from enum import Enum, auto
from functools import wraps
import pickle
import sys

class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DIV = auto()
    MOD = auto()

    OR = auto()
    AND = auto()
    NOT = auto()

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
    BEGIN = auto()
    END = auto()
    VAR = auto()
    PROCEDURE = auto()
    FUNCTION = auto()
    TO = auto()
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
        while self.pos + 1 < self.len and self.text[self.pos + 1].isalnum():
            lexeme += self.next_char()
        if lexeme == 'if':
            return Token(Class.IF, lexeme)
        elif lexeme == 'else':
            return Token(Class.ELSE, lexeme)
        elif lexeme == 'while':
            return Token(Class.WHILE, lexeme)
        elif lexeme == 'for':
            return Token(Class.FOR, lexeme)
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
            token = Token(Class.INT, self.read_int())
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


class Node:
    pass


class Program(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


class Variables(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class ArrayDecl(Node):
    def __init__(self, type_, start_index, end_index, elems):
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


class For(Node):
    def __init__(self, start, end, block):
        self.start = start
        self.end = end
        self.block = block


class Procedure(Node):
    def __init__(self, id_, params, variables, block):
        self.id_ = id_
        self.params = params
        self.variables = variables
        self.block = block


class Function(Node):
    def __init__(self, id_, params, type_, variables, block):
        self.id_ = id_
        self.params = params
        self.type_ = type_
        self.variables = variables
        self.block = block


class Main(Node):
    def __init__(self, variables, block):
        self.variables = variables
        self.block = block


class FuncCall(Node):
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
        self.args = params


class Elems(Node):
    def __init__(self, elems):
        self.elems = elems


class Break(Node):
    pass


class Continue(Node):
    pass


class Exit(Node):
    pass


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
        print(f'{class_}\n')

    def program(self):
        nodes = []
        while self.curr.class_ == Class.PROCEDURE or self.curr.class_ == Class.FUNCTION:
            if self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.procedure_declaration())
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.function_declaration())
            else:
                self.die_deriv(self.program.__name__)
        nodes.append(self.main_declaration())
        return Program(nodes)

    def main_declaration(self):
        vars = None
        if self.curr.class_ == Class.VAR:
            vars = self.variable_declaration_part()
        block = self.block()
        self.eat(Class.DOT)
        return Main(vars, block)

    def procedure_declaration(self):
        self.eat(Class.PROCEDURE)
        id_ = None
        params = []
        self.func_proc_header(id_, params)
        self.eat(Class.SEMICOLON)
        vars = None
        block = None
        self.func_proc_implementation(vars, block)
        return Procedure(id_, params, vars, block)

    def function_declaration(self):
        self.eat(Class.FUNCTION)
        id_ = None
        params = []
        self.func_proc_header(id_, params)
        self.eat(Class.COLON)
        type_ = self.type_()
        self.eat(Class.SEMICOLON)
        vars = None
        block = None
        self.func_proc_implementation(vars, block)
        return Function(id_, params, type_, vars, block)

    def func_proc_header(self, id_, params):
        id_ = self.identifier()
        self.eat(Class.LPAREN)
        while self.curr.class_ == Class.ID:
            params.extend(self.variable_declaration())
            if self.curr.class_ == Class.SEMICOLON:
                self.eat(Class.SEMICOLON)
        self.eat(Class.RPAREN)

    def func_proc_implementation(self, vars, block):
        if self.curr.class_ == Class.VAR:
            vars = self.variable_declaration_part()
        block = self.block()
        self.eat(Class.SEMICOLON)

    def variable_declaration_part(self):
        self.eat(Class.VAR)
        data_type_id = []
        while self.curr.class_ == Class.ID:
            data_type_id.extend(self.variable_declaration())
            self.eat(Class.SEMICOLON)
        return Variables(data_type_id)

    def variable_declaration(self):
        data_type_id = []
        ids = [self.curr.lexeme]
        self.eat(Class.ID)
        while self.curr.class_ != Class.COLON:
            self.eat(Class.COMMA)
            ids.append(self.curr.lexeme)
            self.eat(Class.ID)
        self.eat(Class.COLON)
        data_type = self.type_()
        for id_ in ids:
            data_type_id.append(Decl(data_type, id_))
        return data_type_id

    def identifier(self):
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN and self.is_func_call():
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET and is_array_elem:
            self.eat(Class.LBRACKET)
            index = self.expression()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            expr = self.expression()
            return Assign(id_, expr)
        else:
            return id_

    def if_statement(self):
        self.eat(Class.IF)
        cond = self.logic_expression()
        self.eat(Class.THEN)
        true = self.block()
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            false = self.block()
            self.eat(Class.SEMICOLON)
        else:
            self.eat(Class.SEMICOLON)
        return If(cond, true, false)

    def while_statement(self):
        self.eat(Class.WHILE)
        cond = self.logic_expression()
        self.eat(Class.DO)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return While(cond, block)



    def for_statement(self):
        self.eat(Class.FOR)
        start = self.expression()
        self.eat(Class.TO)
        end = self.expression()
        self.eat(Class.DO)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return For(start, end, block)

    def block(self):
        self.eat(Class.BEGIN)
        nodes = []
        while self.curr.class_ != Class.END:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_statement())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_statement())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_statement())
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
        self.eat(Class.END)
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
        self.eat(Class.SEMICOLON)
        return Exit()

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
        if self.curr.class_ == Class.ARRAY:
            return self.array_type()
        else:
            return self.simple_type()

    def array_type(self):
        self.eat(Class.ARRAY)
        self.eat(Class.LBRACKET)
        start_index = self.curr.lexeme
        self.eat(Class.INT)
        self.eat(Class.DOT)
        self.eat(Class.DOT)
        end_index = self.curr.lexeme
        self.eat(Class.INT)
        self.eat(Class.RBRACKET)
        self.eat(Class.OF)
        type_ = self.simple_type()
        elems = None
        if self.curr.class_ == Class.EQ:
            elems = self.array_element_declaration()
        return ArrayDecl(type_, start_index, end_index, elems)

    def array_element_declaration(self):
        self.eat(Class.EQ)
        self.eat(Class.LPAREN)
        elems = []
        elems.append(self.curr.lexeme)
        self.eat(Class.INT)
        while self.curr.class_ == Class.COMMA:
            self.eat(Class.COMMA)
            elems.append(self.curr.lexeme)
            self.eat(Class.INT)
        self.eat(Class.RPAREN)
        return Elems(elems)

    def simple_type(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
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
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.DIV, Class.MOD]:
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

    def logic_expression(self):
        first = self.compare()
        if self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.OR:
            op = self.curr.lexeme
            self.eat(Class.OR)
            second = self.compare()
            return BinOp(op, first, second)
        else:
            return first

    @restorable
    def is_func_call(self):
        try:
            print('<RESTORABLE>')
            self.eat(Class.LPAREN)
            self.args()
            self.eat(Class.RPAREN)
            return self.curr.class_ != Class.BEGIN
        except:
            return False
        finally:
            print('</RESTORABLE>')

    def parse(self):
        return self.program()

    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))


i = 0
for i in range(1):
    test_id = 11
    path = f'.\\test\\test{test_id}.pas'

    with open(path, 'r') as source:
        text = source.read()

        lexer = Lexer(text)
        tokens = lexer.lex()

        parser = Parser(tokens)
        ast = parser.parse()

        print(ast)
