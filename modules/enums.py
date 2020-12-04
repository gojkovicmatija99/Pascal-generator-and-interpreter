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