from unittest import TestCase, main
from .exercise import Lexer, Token, INTEGER, PLUS, EOF


class TestLexer(TestCase):
    def test_parse_plus(self):
        lexer = Lexer(' 1  + 22 ')
        assert lexer.get_next_token() == Token(INTEGER, 1)
        assert lexer.get_next_token() == Token(PLUS, '+')
        assert lexer.get_next_token() == Token(INTEGER, 22)
        assert lexer.get_next_token() == Token(EOF, None)


if __name__ == "__main__":
    main()