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

    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr_char = self.text[self.pos]
        self.curr_token = None

    def advance(self):
        if self.pos < len(self.text):
            self.curr_char = self.text[self.pos]
        else:
            self.curr_char = None

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


class AST:
    pass


class BinOp(AST):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token: Token):
        self.type = token.type
        self.value = token.value


class Parser(AST):
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.curr_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Error syntax')

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



class translator_RPN:
    def __init__(self, text):
        self.text = text
