"""2020年9月16日16:48:45
"""
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
BLANK = 'BLANK'
EOF = 'EOF'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)


class Interpreter:
    def __init__(self, text):
        self.pos = 0
        self.text = text

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        if self.pos == len(self.text):
            return Token(EOF, None)
        char: str = self.text[self.pos]
        if char.isdigit():
            self.pos += 1
            return Token(INTEGER, int(char))
        if char == '+':
            self.pos += 1
            return Token(PLUS, char)
        if char == '-':
            self.pos += 1
            return Token(MINUS, char)
        if char == ' ':
            self.pos += 1
            return Token(BLANK, char)
        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def skip_blank(self):
        while self.current_token.type == BLANK:
            self.current_token = self.get_next_token()

    def expr(self):
        self.current_token = self.get_next_token()
        self.skip_blank()
        left = self.current_token
        self.eat(INTEGER)
        left2 = None
        try:
            self.skip_blank()
            op = self.current_token
            self.eat(MINUS)
        except:
            op = None
            left2 = self.current_token
            self.eat(INTEGER)
        if op is None:
            self.skip_blank()
            op = self.current_token
            self.eat(MINUS)
        self.skip_blank()
        right = self.current_token
        self.eat(INTEGER)
        try:
            self.skip_blank()
            right2 = self.current_token
            self.eat(INTEGER)
        except:
            right2 = None
            self.eat(EOF)
        if left2 is not None:
            left_value = left.value * 10 + left2.value
        else:
            left_value = left.value
        if right2 is not None:
            right_value = right.value * 10 + right2.value
        else:
            right_value = right.value
        return left_value - right_value


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()