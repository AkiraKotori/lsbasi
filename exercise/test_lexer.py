from unittest import TestCase, main
from exercise import Lexer, Token


class LexerTestCase(TestCase):
    def get_one_token(self, text):
        lexer = Lexer(text)
        return lexer.get_next_token()

    def test_begin(self):
        assert self.get_one_token('BEGIN') == Token('BEGIN', 'BEGIN')

    def test_end(self):
        assert self.get_one_token('END') == Token('END', 'END')

    def test_id(self):
        assert self.get_one_token('identifier') == Token('ID', 'identifier')

    def test_integer(self):
        assert self.get_one_token('123') == Token('INTEGER', 123)

    def test_SEMI(self):
        assert self.get_one_token(';') == Token('SEMI', ';')

    def test_assign(self):
        assert self.get_one_token(':=') == Token('ASSIGN', ':=')

    def test_dot(self):
        assert self.get_one_token('.') == Token('DOT', '.')

    def test_plus(self):
        assert self.get_one_token('+') == Token('PLUS', '+')

    def test_minus(self):
        assert self.get_one_token('-') == Token('MINUS', '-')

    def test_mul(self):
        assert self.get_one_token('*') == Token('MUL', '*')

    def test_div(self):
        assert self.get_one_token('/') == Token('DIV', '/')

    def test_LPAREN(self):
        assert self.get_one_token('(') == Token('LPAREN', '(')

    def test_RPAREN(self):
        assert self.get_one_token(')') == Token('RPAREN', ')')

    def test_eof(self):
        assert self.get_one_token('') == Token('EOF', None)


if __name__ == "__main__":
    main()