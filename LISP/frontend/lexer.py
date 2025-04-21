import re
from enum import Enum, auto
from ply import lex

# Token kinds
class LispTokenKind(Enum):
    PARENTHESE_OPEN = auto()    # "("
    PARENTHESE_CLOSE = auto()   # ")"
    SQUARE_BRACKET_OPEN = auto()  # '['
    SQUARE_BRACKET_CLOSE = auto() # ']'
    SET = auto()                # "set" keyword
    RETURN = auto()             # "return" keyword
    OPERATOR = auto()           # Operators (+, -, *, /)
    TENSOR_OP = auto()          # Tensor operations (e.g. matmul)
    IDENTIFIER = auto()         # Variable names
    NUMBER = auto()             # Numbers (e.g. 42, 3.14)
    EOF = auto()                # End of file token

# Lexer class definition
class LispLexer:
    def __init__(self, input_text):
        self.input = input_text
        self.lexer = lex.lex(module=self)
        self.lexer.input(input_text)
    
    tokens = (
        'PARENTHESE_OPEN',
        'PARENTHESE_CLOSE',
        'SQUARE_BRACKET_OPEN',
        'SQUARE_BRACKET_CLOSE',
        'SET',
        'RETURN',
        'OPERATOR',
        'TENSOR_OP',
        'IDENTIFIER',
        'NUMBER',
    )
    
    t_PARENTHESE_OPEN = r'\('
    t_PARENTHESE_CLOSE = r'\)'
    
    # Keywords
    def t_SET(self, t):
        r'set\b'
        return t
    
    def t_RETURN(self, t):
        r'return\b'
        return t
    
    # Operator - +, -, *, / (do not match '-' when followed by digit)
    def t_OPERATOR(self, t):
        r'(?:\+|\*|/|-(?!\d))'
        return t
    
    # Tensor operations (like matmul, etc.)
    def t_TENSOR_OP(self, t):
        r'(matmul|add|multiply|subtract)\b'  
        return t
    
    # Identifier for variable names
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t
    
    # Numbers (integers and floating point)
    def t_NUMBER(self, t):
        r'-?\d+\.?\d*([eE][+-]?\d+)?'
        return t
    
    # Square bracket tokens
    t_SQUARE_BRACKET_OPEN = r'\['
    t_SQUARE_BRACKET_CLOSE = r'\]'
    
    # Ignore whitespace and comments
    t_ignore = ' \t\r\n'

    # Error handling
    def t_error(self, t):
        raise SyntaxError(f"Illegal character '{t.value[0]}'")
    
    def token(self):
        return self.lexer.token()

    def __iter__(self):
        return self

    def __next__(self):
        token = self.token()
        if not token:
            raise StopIteration
        return token
