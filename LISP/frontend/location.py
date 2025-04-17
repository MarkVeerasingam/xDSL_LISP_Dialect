import re
from dataclasses import dataclass

from typing_extensions import Any

from xdsl.utils.lexer import Token

"""
location.py is a source code location tracker 
a helper module that lets you figure out where in the source code (file, line, column) a given token came from. This is used for:
- error reporting
- debugging
"""

@dataclass
class Location:
    """
    Represents a specific location in a source file.
    Useful for error reporting and diagnostics.
    """
    file: str  # File name where the token appears
    line: int  # Line number
    col: int   # Column number 

    def __repr__(self):
        return f"{self.file}:{self.line}:{self.col}"

# Regex pattern to find newlines, used to compute line and column numbers
_NEWLINE = re.compile(r"\n")


def loc(token: Token[Any]) -> Location:
    """
    Calculates the source code location (file, line, column)
    for a given token using its span data.

    Args:
        token: The token to extract the location from.

    Returns:
        A Location object pointing to the position of the token.

    Raises:
        AssertionError: If the position cannot be calculated.
    """
    file = token.span.input.name # Source file name
    # Could be much faster

    # Offset from the beginning of the input to the start of the token
    remaining = token.span.start
    prev_end = 0 # End position of the last newline

    # Iterate over every newline in the input to determine line and column
    for line, newline_match in enumerate(
        re.finditer(_NEWLINE, token.span.input.content)
    ):
        len_line = newline_match.start() - prev_end
        if remaining < len_line:
            # Found the correct line; calculate column
            return Location(file, line + 1, remaining + 1)
        
        # Move to next line
        remaining -= len_line + 1 # +1 for the newline character
        prev_end = newline_match.end()

    # If we get here, we failed to locate the token in the input
    raise AssertionError(f"Could not find location of token {token}")