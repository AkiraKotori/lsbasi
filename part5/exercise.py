INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __repr__(self) -> str:
        return 'Token({}, {})'.format(self.type, self.value)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr_char = self.text[self.pos]

    def error(self):
        raise Exception('Unknown symbols')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]

    def integer(self):
        result = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        return int(result)

    def get_next_token(self):
        if self.curr_char is None:
            return Token(EOF, None)
        if self.curr_char.isspace():
            self.advance()
            return self.get_next_token()
        if self.curr_char.isdigit():
            return Token(INTEGER, self.integer())
        if self.curr_char == '+':
            self.advance()
            return Token(PLUS, '+')
        if self.curr_char == '-':
            self.advance()
            return Token(MINUS, '-')
        if self.curr_char == '*':
            self.advance()
            return Token(MUL, '*')
        if self.curr_char == '/':
            self.advance()
            return Token(DIV, '/')
        if self.curr_char == '(':
            self.advance()
            return Token(LPAREN, '(')
        if self.curr_char == ')':
            self.advance()
            return Token(RPAREN, ')')
        self.error()


class Interpreter:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.curr_token.type == token_type:
            value = self.curr_token.value
            self.curr_token = self.lexer.get_next_token()
            return value
        self.error()

    def factor(self):
        return self.eat(INTEGER)

    def term(self):
        factor = self.factor()
        while self.curr_token.type != EOF and self.curr_token.type in (MUL,
                                                                       DIV):
            if self.curr_token.type == MUL:
                op = self.eat(MUL)
            else:
                op = self.eat(DIV)
            rfactor = self.factor()
            if op == '*':
                factor *= rfactor
            else:
                factor /= rfactor
        return factor

    def expr(self):
        term = self.term()
        while self.curr_token.type != EOF and self.curr_token.type in (PLUS,
                                                                       MINUS):
            if self.curr_token.type == PLUS:
                op = self.eat(PLUS)
            else:
                op = self.eat(MINUS)
            rterm = self.term()
            if op == '+':
                term += rterm
            else:
                term -= rterm
        return term


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        print(interpreter.expr())


if __name__ == "__main__":
    main()