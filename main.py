import os

from modules.generator import Generator
from modules.lexer import Lexer
from modules.parser import Parser
from modules.grapher import Grapher

cd = os.path.sep
test_id = 8
path = f'test{cd}test{test_id}.pas'

with open(path, 'r') as source:
    text = source.read()

    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()

    # grapher = Grapher(ast)
    # img = grapher.graph()

    generator = Generator(ast)
    code = generator.generate('main.c')