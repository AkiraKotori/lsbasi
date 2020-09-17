"""2020年9月17日
"""

INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVISION = 'DIVISION'
OP_TYPE = [PLUS, MINUS, MULTIPLY, DIVISION]


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr_token = None
        self.curr_char = text[self.pos]
        self.result = None

    def error(self):
        raise Exception('Error parsing text')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()

    def integer(self):
        char = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            char += self.curr_char
            self.advance()
        return int(char)

    def get_next_token(self):
        while self.curr_char is not None:
            curr_char = self.curr_char
            if curr_char.isspace():
                self.skip_whitespace()
                continue
            if curr_char.isdigit():
                return Token(INTEGER, self.integer())
            if curr_char == '+':
                self.advance()
                return Token(PLUS, curr_char)
            if curr_char == '-':
                self.advance()
                return Token(MINUS, curr_char)
            if curr_char == '*':
                self.advance()
                return Token(MULTIPLY, curr_char)
            if curr_char == '/':
                self.advance()
                return Token(DIVISION, curr_char)
            self.error()
        return Token(EOF, None)

    def eat(self, token_type):
        if self.curr_token.type == token_type:
            self.curr_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        if self.result is None:
            self.curr_token = self.get_next_token()
            self.result = self.curr_token
            self.eat(INTEGER)
        left = self.result
        op = self.curr_token
        if op.type in OP_TYPE:
            self.eat(op.type)
        elif op.type == EOF:
            return self.result.value
        else:
            self.error()
        right = self.curr_token
        self.eat(INTEGER)
        if op.type == PLUS:
            self.result = Token(INTEGER, left.value + right.value)
        elif op.type == MINUS:
            self.result = Token(INTEGER, left.value - right.value)
        elif op.type == MULTIPLY:
            self.result = Token(INTEGER, left.value * right.value)
        else:
            self.result = Token(INTEGER, left.value / right.value)
        return self.expr()


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        print(interpreter.expr())


if __name__ == "__main__":
    main()