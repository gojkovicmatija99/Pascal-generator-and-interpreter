from enum import Enum, auto
from functools import wraps
import pickle


class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DOT = auto()
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
    LBRACE = auto()
    RBRACE = auto()

    ASSIGN = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()

    TYPE = auto()
    INT = auto()
    CHAR = auto()
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
    TO = auto()
    DO = auto()
    THEN = auto()

    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()

    ADDRESS = auto()

    ID = auto()
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

    def isOnlyOneChar(self):
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
        elif lexeme == 'return':
            return Token(Class.RETURN, lexeme)
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
        elif lexeme == 'integer' or lexeme == 'char' or lexeme == 'void':
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
            if self.isOnlyOneChar():
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
        elif curr == '/':
            token = Token(Class.FWDSLASH, curr)
        elif curr == '%':
            token = Token(Class.PERCENT, curr)
        elif curr == '&':
            curr = self.next_char()
            if curr == '&':
                token = Token(Class.AND, '&&')
            else:
                token = Token(Class.ADDRESS, '&')
                self.pos -= 1
        elif curr == '|':
            curr = self.next_char()
            if curr == '|':
                token = Token(Class.OR, '||')
            else:
                self.die(curr)
        elif curr == '!':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.NEQ, '!=')
            else:
                token = Token(Class.NOT, '!')
                self.pos -= 1
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
        elif curr == '{':
            token = Token(Class.LBRACE, curr)
        elif curr == '}':
            token = Token(Class.RBRACE, curr)
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


class Node():
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
    def __init__(self, type_, id_, size, elems):
        self.type_ = type_
        self.id_ = id_
        self.size = size
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

class FuncImpl(Node):
    def __init__(self, type_, id_, params, block):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.block = block


class FuncCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Params(Node):
    def __init__(self, params):
        self.params = params


class Args(Node):
    def __init__(self, args):
        self.args = args


class Elems(Node):
    def __init__(self, elems):
        self.elems = elems


class Break(Node):
    pass


class Continue(Node):
    pass


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Type(Node):
    def __init__(self, value):
        self.value = value


class Int(Node):
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
        while self.curr.class_ != Class.DOT:
            if self.curr.class_ == Class.BEGIN:
                nodes.append(self.block())
            elif self.curr.class_ == Class.VAR:
                nodes.append(self.variable_declaration_part())
            elif self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.procedure_declaration_part())
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)

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
        data_type = self.curr.lexeme
        for id_ in ids:
            data_type_id.append(Decl(data_type, id_))
        self.eat(Class.TYPE)
        return data_type_id

    def procedure_declaration_part(self):
        pass

    def id_(self):
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
            index = self.expr()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            expr = self.expr()
            return Assign(id_, expr)
        else:
            return id_

    def decl(self):
        type_ = self.type_()
        id_ = self.id_()
        if self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            size = None
            if self.curr.class_ != Class.RBRACKET:
                size = self.expr()
            self.eat(Class.RBRACKET)
            elems = None
            if self.curr.class_ == Class.ASSIGN:
                self.eat(Class.ASSIGN)
                self.eat(Class.LBRACE)
                elems = self.elems()
                self.eat(Class.RBRACE)
            self.eat(Class.SEMICOLON)
            return ArrayDecl(type_, id_, size, elems)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            params = self.params()
            self.eat(Class.RPAREN)
            self.eat(Class.LBRACE)
            block = self.block()
            self.eat(Class.RBRACE)
            return FuncImpl(type_, id_, params, block)
        else:
            self.eat(Class.SEMICOLON)
            return Decl(type_, id_)

    def if_(self):
        self.eat(Class.IF)
        self.eat(Class.LPAREN)
        cond = self.logic()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        true = self.block()
        self.eat(Class.RBRACE)
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            self.eat(Class.LBRACE)
            false = self.block()
            self.eat(Class.RBRACE)
        return If(cond, true, false)

    def while_(self):
        self.eat(Class.WHILE)
        self.eat(Class.LPAREN)
        cond = self.logic()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        block = self.block()
        self.eat(Class.RBRACE)
        return While(cond, block)

    def for_(self):
        self.eat(Class.FOR)
        start = self.expr()
        self.eat(Class.TO)
        end = self.expr()
        self.eat(Class.DO)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return For(start, end, block)

    def block(self):
        self.eat(Class.BEGIN)
        nodes = []
        while self.curr.class_ != Class.END:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.RETURN:
                nodes.append(self.return_())
            elif self.curr.class_ == Class.TYPE:
                nodes.append(self.decl())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        self.eat(Class.END)
        return Block(nodes)

    def params(self):
        params = []
        while self.curr.class_ != Class.RPAREN:
            if len(params) > 0:
                self.eat(Class.COMMA)
            type_ = self.type_()
            id_ = self.id_()
            params.append(Decl(type_, id_))
        return Params(params)

    def args(self):
        args = []

        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            args.append(self.expr())
            if self.curr.class_ == Class.INT:
                self.eat(Class.INT)
            elif self.curr.class_ == Class.CHAR:
                self.eat(Class.CHAR)
            elif self.curr.class_ == Class.STRING:
                self.eat(Class.STRING)
        return Args(args)

    def elems(self):
        elems = []
        while self.curr.class_ != Class.RBRACE:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(self.expr())
            if self.curr.class_ == Class.INT:
                self.eat(Class.INT)
            elif self.curr.class_ == Class.CHAR:
                self.eat(Class.CHAR)
            elif self.curr.class_ == Class.STRING:
                self.eat(Class.STRING)
        return Elems(elems)

    def return_(self):
        self.eat(Class.RETURN)
        expr = self.expr()
        self.eat(Class.SEMICOLON)
        return Return(expr)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
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
        elif self.curr.class_ == Class.ID:
            return self.id_()
        elif self.curr.class_ in [Class.MINUS, Class.NOT, Class.ADDRESS]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
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

    def expr(self):
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
        first = self.expr()
        if self.curr.class_ == Class.EQ:
            op = self.curr.lexeme
            self.eat(Class.EQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(op, first, second)
        else:
            return first

    def logic(self):
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
            print('</RESTORABLE>')
            return self.curr.class_ != Class.BEGIN
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


test_id = 4
path = f'C:\\Users\\Matija\\Downloads\\test\\test{test_id}.pas'

with open(path, 'r') as source:
    text = source.read()

    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()

    print(ast)
