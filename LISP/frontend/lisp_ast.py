from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union

from .location import Location  

class ExprASTKind(Enum):
    VarDecl = auto()    # "(set x 5)"
    Return = auto()     # "(return x)"
    Num = auto()        # "10"
    Var = auto()        # "x"
    BinOp = auto()      # "(+ x 2)"

@dataclass
class VarType:
    shape: int  # Keeping it simple for now. will make it a list later

# base class for all expressions
@dataclass
class ExprAST:
    loc: Location

    @property
    def kind(self) -> ExprASTKind:
        raise NotImplementedError("Subclasses should implement this!")

# variable declarations (e.g., (set x 5))
@dataclass
class VarDeclExprAST(ExprAST):
    name: str
    var_type: VarType
    expr: ExprAST  # Expression assigned to the variable

    @property
    def kind(self):
        return ExprASTKind.VarDecl

# numeric expressions (e.g., 10)
@dataclass
class NumberExprAST(ExprAST):
    val: float  # The numeric value

    @property
    def kind(self):
        return ExprASTKind.Num

# variable references (e.g., x)
@dataclass
class VariableExprAST(ExprAST):
    name: str  # Variable name

    @property
    def kind(self):
        return ExprASTKind.Var

# binary operations (e.g., (+ x 2))
@dataclass
class BinaryExprAST(ExprAST):
    op: str  # The operator (e.g., +, -, *, /)
    lhs: ExprAST  # Left-hand side expression
    rhs: ExprAST  # Right-hand side expression

    @property
    def kind(self):
        return ExprASTKind.BinOp

# return statements (e.g., (return x))
@dataclass
class ReturnExprAST(ExprAST):
    expr: ExprAST  # Expression to return

    @property
    def kind(self):
        return ExprASTKind.Return