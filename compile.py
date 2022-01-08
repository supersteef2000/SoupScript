from lex import *
from emit import *
from parse import *
import sys


def main():
    print("SoupScript v5000 © 2022 all rights reserved")
    # list comp + 4 lüp     let without value = input?     # ,, as var   allow «» as var?    check for double ,, done?

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")

    with open(sys.argv[1], 'r', encoding="utf-8") as input_file:
        input = input_file.read()

    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.write_file()


main()
