from pathlib import Path
from typing import cast

from xdsl.parser import GenericParser, ParserState
from xdsl.utils.lexer import Input

# from .lexer import LispLexer, LispToken, LispTokenKind
from .location import loc
from .lisp_ast import (
    BinaryExprAST,
    ExprAST,
    NumberExprAST,
    ReturnExprAST,
    VarDeclExprAST,
    VariableExprAST,
    VarType,
)