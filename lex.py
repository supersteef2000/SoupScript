import enum
import sys


class Lexer:
    def __init__(self, input):
        self.source = input
        self.cur_char = ''
        self.cur_pos = -1
        self.next_char()
        self.list = []

    # Process next character
    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'  # EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    # Return lookahead character
    def peek(self):
        if self.cur_pos + 1 >= len(self.source):
            return '\0'

        return self.source[self.cur_pos + 1]

    # Invalid token found, rage-quit time
    def abort(self, message):
        sys.exit("Lexing error: " + message)

    def skip_period_and_comma(self):
        while self.cur_char == '.' or self.cur_char == ',':
            self.next_char()
            if self.cur_char == '\n':
                self.next_char()

    # Skip comments
    def skip_comment(self):
        if self.cur_char == '|':
            self.next_char()
            while self.cur_char != '|':
                self.next_char()
            self.next_char()

    def is_cursed(self):
        return self.cur_char == 'b' or self.cur_char == '0' or self.cur_char == '+' or self.cur_char == '-'\
               or self.cur_char == '/' or self.cur_char == '=' or self.cur_char == '>' or self.cur_char == '<'\
               or self.cur_char == '>' or self.cur_char == '!' or self.cur_char == '?' or self.cur_char == 'p' \
               or self.cur_char == '$'

        # Return next token

    def get_token(self):
        global cur_pos
        while self.cur_char == '.' or self.cur_char == ',' or self.cur_char == '|':
            self.skip_period_and_comma()
            self.skip_comment()
        token = None

        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == '=':
            token = Token(self.cur_char, TokenType.EQEQ)
        elif self.cur_char == '%':
            if self.peek() == '%':
                token = Token(self.cur_char, TokenType.INPUT)
                self.next_char()
            else:
                token = Token(self.cur_char, TokenType.MODULO)
        elif self.cur_char == 'b':
            if self.peek() == ',':
                start_pos = self.cur_pos
                self.next_char()
                while self.peek() != ',' or self.is_cursed():
                    self.next_char()
                    if self.peek() == '\0':
                        break
                tok_text = self.source[start_pos : self.cur_pos + 1]
                token = Token(tok_text, TokenType.IDENT)
            else:
                token = Token(self.cur_char, TokenType.EQ)
        elif self.cur_char == 'p':
            if self.peek() == ',':
                start_pos = self.cur_pos
                self.next_char()
                while self.peek() != ',' or self.is_cursed():
                    self.next_char()
                    if self.peek() == '\0':
                        break
                tok_text = self.source[start_pos : self.cur_pos + 1]
                token = Token(tok_text, TokenType.IDENT)
            else:
                token = Token(self.cur_char, TokenType.PRINT)
                self.list.append("print")
        elif self.cur_char == '>':
            token = Token(self.cur_char, TokenType.GT)
        elif self.cur_char == '<':
            token = Token(self.cur_char, TokenType.LT)
        elif self.cur_char == '$':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '?':
            token = Token(self.cur_char, TokenType.IF)
            self.list.append("if")
        elif self.cur_char == '&':
            token = Token(self.cur_char, TokenType.WHILE)
            self.list.append("while")
        elif self.cur_char == ';':
            if self.list[len(self.list) - 1] == "if":
                self.list.pop()
                token = Token(self.cur_char, TokenType.ENDIF)
            elif self.list[len(self.list) - 1] == "while":
                self.list.pop()
                token = Token(self.cur_char, TokenType.ENDWHILE)
            elif self.list[len(self.list) - 1] == "print":
                self.list.pop()
                token = Token(self.cur_char, TokenType.ENDPRINT)
        elif self.cur_char == '!':
            if self.peek() == '<':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char + self.cur_char, TokenType.GTEQ)
            elif self.peek() == '>':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char + self.cur_char, TokenType.LTEQ)
            elif self.peek() == '!':
                self.next_char()
                if self.list[len(self.list) - 1] == "if":
                    token = Token(self.cur_char, TokenType.THEN)
                elif self.list[len(self.list) - 1] == "while":
                    token = Token(self.cur_char, TokenType.REPEAT)
                elif self.list[len(self.list) - 1] == "print":
                    token = Token(self.cur_char, TokenType.STARTPRINT)
                else:
                    self.abort("Lonely !! found but not expected.")
            else:
                token = Token(self.cur_char, TokenType.NOTEQ)
        elif self.cur_char == '0':
            if self.peek().isdigit():
                self.next_char()
                start_pos = self.cur_pos
                while self.peek().isdigit():
                    self.next_char()
                is_int = False
                if self.peek() == '.':
                    cur_pos = self.cur_pos
                    self.next_char()
                    if not self.peek().isdigit():
                        is_int = True
                    else:
                        is_int = False
                    while self.peek().isdigit():
                        self.next_char()
                if is_int:
                    self.cur_pos = cur_pos
                tok_text = self.source[start_pos : self.cur_pos + 1]
                token = Token(tok_text, TokenType.NUMBER)
            else:
                start_pos = self.cur_pos
                while self.peek() != ',' or self.is_cursed():
                    self.next_char()
                    if self.peek() == '\0':
                        break
                tok_text = self.source[start_pos : self.cur_pos + 1]
                token = Token(tok_text, TokenType.IDENT)
        elif self.cur_char.isalnum() or self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\n' or self.cur_char == '\r':
            start_pos = self.cur_pos
            while self.peek() != ',' or self.is_cursed():
                self.next_char()
                if self.peek() == '\0':
                    break
            tok_text = self.source[start_pos : self.cur_pos + 1]
            token = Token(tok_text, TokenType.IDENT)
        elif self.cur_char == '«':
            self.next_char()
            start_pos = self.cur_pos

            while self.cur_char != '»':
                self.next_char()
            tok_text = self.source[start_pos : self.cur_pos]
            token = Token(tok_text, TokenType.STRING)
        elif self.cur_char == '\0':
            token = Token('', TokenType.EOF)
        else:
            # what even am I looking at
            self.abort("Unknown token: " + self.cur_char)
        if token.kind == TokenType.IDENT:
            token.text = token.text.translate(str.maketrans(token.text, token.text, ','))
        self.next_char()
        return token


class Token:
    def __init__(self, token_text, token_kind):
        self.text = token_text  # token text
        self.kind = token_kind  # token kind


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    STARTPRINT = 104
    ENDPRINT = 105
    INPUT = 106
    LET = 107
    IF = 108
    THEN = 109
    ENDIF = 110
    WHILE = 111
    REPEAT = 112
    ENDWHILE = 113
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    MODULO = 212
