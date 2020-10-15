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
        self.pos += 1
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
        self.token = token
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
        if curr_token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        node = self.factor()
        while self.curr_token.type in (MUL, DIV):
            curr_token = self.curr_token
            if self.curr_token.type == MUL:
                self.eat(MUL)
            elif self.curr_token.type == DIV:
                self.eat(DIV)
            node = BinOp(node, curr_token, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.curr_token.type in (PLUS, MINUS):
            curr_token = self.curr_token
            if self.curr_token.type == PLUS:
                self.eat(PLUS)
            elif self.curr_token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(node, curr_token, self.term())
        return node


result = []


def translator_RPN(node):
    if isinstance(node, Num):
        result.append(node.value)
    else:
        translator_RPN(node.left)
        translator_RPN(node.right)
        result.append(node.op.value)


def calc(left, op, right):
    return eval('{}{}{}'.format(left, op, right))


def calc_RPN(text):
    global result
    stack = []
    for elem in result:
        if isinstance(elem, int):
            stack.append(elem)
        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(calc(left, elem, right))
    print('result: {} = {}'.format(eval(text), stack.pop()))
    result = []


def check_RPN(text):
    parser = Parser(text)
    node = parser.expr()
    translator_RPN(node)
    calc_RPN(text)


def translator_RPN2(node):
    if isinstance(node,Num):
        return node.value
    else:
        left=translator_RPN2(node.left)
        right=translator_RPN2(node.right)
        op=node.op.value
        return '{} {} {}'.format(left,right,op)

def check_RPN2(text):
    parser = Parser(text)
    node = parser.expr()
    print(translator_RPN2(node))


def translator_LISP(node):
    if isinstance(node,Num):
        return node.value
    else:
        left=translator_LISP(node.left)
        op=node.op.value
        right=translator_LISP(node.right)
        return '({} {} {})'.format(op,left,right)
    
def check_LISP(text):
    parser = Parser(text)
    node = parser.expr()
    print(translator_LISP(node))


if __name__ == "__main__":
    # check_RPN2('1+2*3+4/5-6*7/8+9/10')
    # check_RPN2('1')
    # check_RPN2('22/33')
    # check_RPN2('(1+2)/3*4+5-6')
    # check_RPN2('(1*(2+3)-4)+6/8')
    check_LISP('1+2*3+4/5-6*7/8+9/10')
    check_LISP('7 + 5 * 2 - 3')
    check_LISP('22/33')
    check_LISP('(1+2)/3*4+5-6')
    check_LISP('(1*(2+3)-4)+6/8')