from xdsl.utils.lexer import Input
from LISP.frontend.lexer import LispLexer
import unittest

class TestLispLexer(unittest.TestCase):

    def test_lexer(self):
        text = "(set x 42)"
        input_obj = Input(text, "<test>")
        lexer = LispLexer(input_obj)

        tokens = []
        while True:
            token = lexer.lex()
            tokens.append(token)
            if token.kind.name == "EOF":
                break

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "SET", "IDENTIFIER", "NUMBER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.kind.name for token in tokens], expected_token_kinds)

    def test_lexer_with_operators(self):
        text = "(+ 3 4)"
        input_obj = Input(text, "<test>")
        lexer = LispLexer(input_obj)

        tokens = []
        while True:
            token = lexer.lex()
            tokens.append(token)
            if token.kind.name == "EOF":
                break

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "OPERATOR", "NUMBER", "NUMBER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.kind.name for token in tokens], expected_token_kinds)

    def test_lexer_with_return_keyword(self):
        text = "(return x)"
        input_obj = Input(text, "<test>")
        lexer = LispLexer(input_obj)

        tokens = []
        while True:
            token = lexer.lex()
            tokens.append(token)
            if token.kind.name == "EOF":
                break

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "RETURN", "IDENTIFIER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.kind.name for token in tokens], expected_token_kinds)

    def test_lexer_nested(self):
        text = "(* (+ 1 2) (+ 2 1))"
        input_obj = Input(text, "<test>")
        lexer = LispLexer(input_obj)

        tokens = []
        while True:
            token = lexer.lex()
            tokens.append(token)
            if token.kind.name == "EOF":
                break
