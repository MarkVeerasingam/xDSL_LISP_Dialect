import re
from enum import Enum, auto
from typing import TypeAlias

from xdsl.utils.exceptions import ParseError
from xdsl.utils.lexer import Lexer, Position, Span, Token, Input

# Token kinds
class LispTokenKind(Enum):
    PARENTHESE_OPEN = auto()    # "("
    PARENTHESE_CLOSE = auto()   # ")"
    SET = auto()                # "set" keyword
    RETURN = auto()             # "return" keyword
    IDENTIFIER = auto()         # Variable names
    NUMBER = auto()             # Numbers (e.g. 42, 3.14)
    OPERATOR = auto()           # Operators (+, -, *, /)
    EOF = auto()                # End of file token

# Single character tokens (punctuation)
SINGLE_CHAR_TOKENS = {
    "(": LispTokenKind.PARENTHESE_OPEN,
    ")": LispTokenKind.PARENTHESE_CLOSE,
    "+": LispTokenKind.OPERATOR,
    "-": LispTokenKind.OPERATOR,
    "*": LispTokenKind.OPERATOR,
    "/": LispTokenKind.OPERATOR,
}

# Keywords mapping
KEYWORDS = {
    "set": LispTokenKind.SET,
    "return": LispTokenKind.RETURN
}

LispToken: TypeAlias = Token[LispTokenKind]

class LispLexer(Lexer[LispTokenKind]):
    def __init__(self, input: Input):
        super().__init__(input)
        self.parentheses_count = 0  # Initialize a counter for open parentheses.

    def _is_in_bounds(self, size: Position = 1) -> bool:
        """Check if the current position is within the bounds of the input."""
        return self.pos + size - 1 < self.input.len
    
    def _get_chars(self, size: int = 1) -> str | None:
        """Get the character at the current location, or multiple characters ahead."""
        res = self.input.slice(self.pos, self.pos + size)
        self.pos += size
        return res

    def _peek_chars(self, size: int = 1) -> str | None:
        """Peek at the character at the current location, or multiple characters ahead."""
        return self.input.slice(self.pos, self.pos + size)

    def _consume_chars(self, size: int = 1) -> None:
        """Advance the lexer position in the input by the given amount."""
        self.pos += size

    def _consume_regex(self, regex: re.Pattern[str]) -> re.Match[str] | None:
        """Advance the lexer position to the end of the next match of the given regex."""
        match = regex.match(self.input.content, self.pos)
        if match is None:
            return None
        self.pos = match.end()
        return match

    _whitespace_regex = re.compile(r"\s+", re.ASCII)
    
    def _consume_whitespace(self) -> None:
        """Consume whitespace."""
        self._consume_regex(self._whitespace_regex)

    def lex(self) -> LispToken:
        # Skip whitespaces
        self._consume_whitespace()

        start_pos = self.pos
        current_char = self._get_chars()

        # Handle end of file
        if current_char is None:
            if self.parentheses_count != 0:  # Check if there are unmatched parentheses.
                raise ParseError(
                    Span(start_pos, self.pos, self.input),
                    "Unmatched parentheses"
                )
            return self._form_token(LispTokenKind.EOF, start_pos)

        # Single-char punctuation 
        single_char_token_kind = SINGLE_CHAR_TOKENS.get(current_char)
        if single_char_token_kind is not None:
            return self._form_token(single_char_token_kind, start_pos)

        # Numbers
        if current_char.isdigit() or (current_char == '-' and self._is_in_bounds() and self._peek_chars().isdigit()):
            return self._lex_number(start_pos)

        # Identifiers and keywords
        if current_char.isalpha() or current_char == '_':
            return self._lex_identifier_or_keyword(start_pos)

        raise ParseError(
            Span(start_pos, start_pos + 1, self.input),
            f"Unexpected character: {current_char}",
        )
    
    IDENTIFIER_SUFFIX = r"[a-zA-Z0-9_]*"
    identifier_suffix_regex = re.compile(IDENTIFIER_SUFFIX)

    def _lex_identifier_or_keyword(self, start_pos: Position) -> LispToken:
        """Lex an identifier or keyword."""
        # Save the position before consuming more characters
        identifier_start = self.pos - 1
        
        # Consume the rest of the identifier
        self._consume_regex(self.identifier_suffix_regex)
        
        # Extract the complete identifier string
        identifier = self.input.slice(identifier_start, self.pos)
        
        # Check if it's a keyword
        if identifier in KEYWORDS:
            return self._form_token(KEYWORDS[identifier], start_pos)
        
        # It's a regular identifier
        return self._form_token(LispTokenKind.IDENTIFIER, start_pos)

    _digits_star_regex = re.compile(r"[0-9]*")
    _fractional_suffix_regex = re.compile(r"\.[0-9]*([eE][+-]?[0-9]+)?")

    def _lex_number(self, start_pos: Position) -> LispToken:
        """Lex a number literal."""
        # Consume digits
        self._consume_regex(self._digits_star_regex)

        # Check if we are lexing a floating point
        self._consume_regex(self._fractional_suffix_regex)
        
        return self._form_token(LispTokenKind.NUMBER, start_pos)
