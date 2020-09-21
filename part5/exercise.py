from part5.calc5 import PLUS

INTEGER = 'INTEGER'
EOF = 'EOF'
PULS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr_char = self.text[self.pos]

    def advance(self, text):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_char = None
        self.curr_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        return int(result)

    def get_next_token(self):
        if self.curr_char.isspace():
            self.skip_whitespace()
            self.get_next_token()
        if self.curr_char.isdigit():
            return Token(INTEGER, self.integer())
        if self.curr_char == '+':
            return Token(PLUS, '+')
        if self.curr_char == '-':
            return Token(MINUS, '-')
        if self.curr_char == '*':
            return Token(MUL, '*')
        if self.curr_char == '/':
            return Token(DIV, '/')
