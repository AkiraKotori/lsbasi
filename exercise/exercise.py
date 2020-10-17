BEGIN, END, SEMI, ASSIGN, ID, DOT, EOF = ('BEGIN', 'END', 'SEMI', 'ASSIGN',
                                          'ID', 'DOT', 'EOF')
PLUS, MINUS, MUL, DIV, LPAREN, RPAREN = ('PLUS', 'MINUS', 'MUL', 'DIV',
                                         'LPAREN', 'RPAREN')
INTEGER = ('INTEGER')


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False


RESERVED_KEYWORDS = {'BEGIN': Token(BEGIN, 'BEGIN'), 'END': Token(END, 'END')}


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        if self.text:
            self.curr_char = self.text[self.pos]
        else:
            self.curr_char = None

    def error(self):
        raise Exception('Invalid Term')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        result = ''
        while self.curr_char is not None and self.curr_char.isalnum():
            result += self.curr_char
            self.advance()
        return RESERVED_KEYWORDS.get(result, Token(ID, result))

    def integer(self):
        result = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        return Token(INTEGER, int(result))

    def get_next_token(self):
        if self.curr_char is None:
            return Token(EOF, None)
        if self.curr_char.isspace():
            self.advance()
            return self.get_next_token()
        if self.curr_char.isalpha():
            return self._id()
        if self.curr_char.isdigit():
            return self.integer()
        if self.curr_char == ';':
            self.advance()
            return Token(SEMI, ';')
        if self.curr_char == ':':
            if self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
        if self.curr_char == '.':
            self.advance()
            return Token(DOT, '.')
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


class AST:
    pass


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class NoOp(AST):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid Syntax')

    def eat(self, type):
        if self.curr_token.type == type:
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        curr_token = self.curr_token
        if curr_token.type == INTEGER:
            self.eat(INTEGER)
            return Num(curr_token)
        if curr_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        if curr_token.type in (PLUS, MINUS):
            if curr_token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)
            return UnaryOp(curr_token, self.factor())

    def term(self):
        node = self.factor()
        while self.curr_token.type in (MUL, DIV):
            curr_token = self.curr_token
            if curr_token.type == MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)
            node = BinOp(node, curr_token, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.curr_token.type in (PLUS, MINUS):
            curr_token = self.curr_token
            if curr_token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)
            node = BinOp(node, curr_token, self.term())
        return node


if __name__ == "__main__":
    lexer = Lexer('-+-+22++-33')
    parser = Parser(lexer)
    node = parser.expr()
    print(node)
