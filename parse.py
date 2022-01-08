import sys
from lex import *


class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()

        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

    def check_token(self, kind):
        return kind == self.cur_token.kind

    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            self.abort("Expected " + kind.name + ", got " + self.cur_token.kind.name)
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        sys.exit("Parsing error: " + message)

    def program(self):
        self.emitter.header_line("#include <stdio.h>")
        self.emitter.header_line("int main(void){")

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

    def statement(self):
        if self.check_token(TokenType.PRINT):
            self.next_token()
            if self.check_token(TokenType.NEWLINE):
                self.nl()
            self.match(TokenType.STARTPRINT)
            if self.check_token(TokenType.NEWLINE):
                self.nl()
            if self.check_token(TokenType.STRING):
                self.emitter.emit_line("printf(\"" + self.cur_token.text + "\");")
                self.next_token()
            else:
                self.emitter.emit("printf(\"%" + "i\", (int)(")
                self.expression()
                self.emitter.emit_line("));")
            if self.check_token(TokenType.NEWLINE):
                self.nl()
            self.match(TokenType.ENDPRINT)
        elif self.check_token(TokenType.IF):
            self.next_token()
            self.emitter.emit("if (")
            self.comparison()

            self.match(TokenType.THEN)
            self.emitter.emit_line(") {")

            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emit_line("}")
        elif self.check_token(TokenType.WHILE):
            self.next_token()
            self.emitter.emit("while (")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.emitter.emit_line(") {")

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emit_line("}")
        elif self.check_token(TokenType.INPUT):
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line("int " + self.cur_token.text + ";")

            self.emitter.emit_line("if (0 == scanf_s(\"%" + "i\", &" + self.cur_token.text + ")) {")
            self.emitter.emit_line(self.cur_token.text + " = 0;")
            self.emitter.emit("scanf_s(\"%")
            self.emitter.emit_line("*s\");")
            self.emitter.emit_line("}")
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.IDENT):
            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line("int " + self.cur_token.text + ";")

            self.emitter.emit(self.cur_token.text + " = ")
            self.next_token()
            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emit_line(";")
        else:
            self.abort("Invalid statement at " + self.cur_token.text + " (" + self.cur_token.kind.name + ")")

    def nl(self):
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def comparison(self):
        self.expression()

        match self.cur_token.text:
            case '=': self.cur_token.text = '=='
            case '!<': self.cur_token.text = '>='
            case '!>': self.cur_token.text = '<='
            case '!': self.cur_token.text = '!='
            case _: ()

        if self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()

        while self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()
    
    def is_comparison_operator(self):
        return self.check_token(TokenType.GT) or self.check_token(TokenType.GTEQ)\
               or self.check_token(TokenType.LT) or self.check_token(TokenType.LTEQ)\
               or self.check_token(TokenType.EQEQ) or self.check_token(TokenType.NOTEQ)

    def expression(self):
        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.term()

    def term(self):
        self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH) or self.check_token(TokenType.MODULO):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.unary()

    def unary(self):
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        self.primary()

    def primary(self):
        if self.check_token(TokenType.NUMBER):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.cur_token.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.cur_token.text)
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        else:
            self.abort("Unexpected token at " + self.cur_token.text)
