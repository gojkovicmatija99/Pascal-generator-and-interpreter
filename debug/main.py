from modules.generator import Generator
from modules.grapher import Grapher
from modules.lexer import Lexer
from modules.parser import Parser
from modules.runner import Runner
from modules.symbolizer import Symbolizer

DEBUG = True  # OBAVEZNO: Postaviti na False pre slanja projekta

if DEBUG:
    test_id = '12'  # Redni broj test primera [01-15]
    path_root = './'
    args = {}
    args['src'] = f'{path_root}{test_id}/src.pas'  # Izvorna PAS datoteka
    args['gen'] = f'{path_root}{test_id}/gen.c'  # Generisana C datoteka
else:
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
    # grapher = Grapher(ast)
    # grapher.graph()
    symbolizer = Symbolizer(ast)
    symbolizer.symbolize()
    generator = Generator(ast)
    generator.generate(args['gen'])
    runner = Runner(ast)
    runner.run()

# ACINONYX - END
