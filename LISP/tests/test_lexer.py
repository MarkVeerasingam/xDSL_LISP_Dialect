from LISP.frontend.lexer import LispLexer
import unittest

class TestLispLexer(unittest.TestCase):

    def test_lexer(self):
        text = "(set x 42)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "SET", "IDENTIFIER", "NUMBER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_lexer_with_operators(self):
        text = "(+ 3 4)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "OPERATOR", "NUMBER", "NUMBER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_lexer_with_negative_operators(self):
        text = "(- 3.9 4.1)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "OPERATOR", "NUMBER", "NUMBER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_lexer_with_return_keyword(self):
        text = "(return x)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "RETURN", "IDENTIFIER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_lexer_nested(self):
        text = "(* (+ 1 2) (+ 2 1))"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        print([token.type for token in tokens])
        
        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "OPERATOR", "PARENTHESE_OPEN", "OPERATOR", "NUMBER", "NUMBER", 
            "PARENTHESE_CLOSE", "PARENTHESE_OPEN", "OPERATOR", "NUMBER", "NUMBER", "PARENTHESE_CLOSE", 
            "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_tensor_literal(self):
        text = "(set A ([1 2] [3 4]))"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)
        
        print([token.type for token in tokens])

        # Updated expected token sequence reflecting the actual token order
        expected_token_kinds = [
            "PARENTHESE_OPEN", "SET", "IDENTIFIER", "PARENTHESE_OPEN", "SQUARE_BRACKET_OPEN", "NUMBER", 
            "NUMBER", "SQUARE_BRACKET_CLOSE", "SQUARE_BRACKET_OPEN", "NUMBER", "NUMBER", 
            "SQUARE_BRACKET_CLOSE", "PARENTHESE_CLOSE", "PARENTHESE_CLOSE", "EOF"
        ]
        
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_tensor_literal_diff_dimensions(self):
        text = "(set B ([1 2 3] [-4 5 6]))"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)
        
        print([token.type for token in tokens])

        # Expected token sequence
        expected_token_kinds = [
            "PARENTHESE_OPEN", "SET", "IDENTIFIER", "PARENTHESE_OPEN", "SQUARE_BRACKET_OPEN", 
            "NUMBER", "NUMBER", "NUMBER", "SQUARE_BRACKET_CLOSE", "SQUARE_BRACKET_OPEN", 
            "NUMBER", "NUMBER", "NUMBER", "SQUARE_BRACKET_CLOSE", "PARENTHESE_CLOSE", 
            "PARENTHESE_CLOSE", "EOF"
        ]
        
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_tensor_literal_negative_numbers(self):
        text = "(set C ([-1 -2] [3 4]))"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)
        
        print([token.type for token in tokens])

        # Expected token sequence
        expected_token_kinds = [
            "PARENTHESE_OPEN", "SET", "IDENTIFIER", "PARENTHESE_OPEN", "SQUARE_BRACKET_OPEN", 
            "NUMBER", "NUMBER", "SQUARE_BRACKET_CLOSE", "SQUARE_BRACKET_OPEN", "NUMBER", 
            "NUMBER", "SQUARE_BRACKET_CLOSE", "PARENTHESE_CLOSE", "PARENTHESE_CLOSE", "EOF"
        ]
        
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_tensor_operation(self):
        text = "(matmul A B)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)
        
        # Print the lexed tokens for debugging
        print([token.type for token in tokens])

        expected_token_kinds = [
            "PARENTHESE_OPEN", "TENSOR_OP", "IDENTIFIER", "IDENTIFIER", "PARENTHESE_CLOSE", "EOF"
        ]
        
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_tensor_subtraction_operation(self):
        text = "(subtract A B)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "TENSOR_OP", "IDENTIFIER", "IDENTIFIER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_tensor_addition_operation(self):
        text = "(add A B)"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "TENSOR_OP", "IDENTIFIER", "IDENTIFIER", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)

    def test_singular_complex_tensor(self):
        text = "(set D ([1]))"
        lexer = LispLexer(text)

        tokens = []
        while True:
            token = lexer.token()  # Get next token
            if token is None:
                break
            tokens.append(token)

        # Assert the lexed tokens match the expected output
        expected_token_kinds = [
            "PARENTHESE_OPEN", "SET", "IDENTIFIER", "PARENTHESE_OPEN", "SQUARE_BRACKET_OPEN", "NUMBER", 
            "SQUARE_BRACKET_CLOSE", "PARENTHESE_CLOSE", "PARENTHESE_CLOSE", "EOF"
        ]
        self.assertEqual([token.type for token in tokens] + ["EOF"], expected_token_kinds)
