from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union, List

from .location import Location  

class ExprASTKind(Enum):
    VarDecl = auto()    # "(set x 5)"
    Return = auto()     # "(return x)"
    Num = auto()        # "10"
    Var = auto()        # "x"
    BinOp = auto()      # "(+ x 2)"
    TensorLiteral = auto() # Tensor ([1 2] [3 4])
    TensorOp = auto()   # e.g. matmul or addition

@dataclass
class VarType:
    shape: int

@dataclass 
class TensorVarType: 
    shape: list[int] # (e.g., [2, 2] for a 2x2 tensor)

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
    val: float  # The numeric literal value

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

# tensor operations
"""
--Tensor Operations--
(set A ([1 2] [3 4]) : tensor<2x2xi64>)
(set B ([5 6] [7 8]) : tensor<2x2xi64>)
"""
@dataclass
class TensorLiteralExprAST(ExprAST):
    elements: List[List[Union[float, int]]]
    tensor_type: TensorVarType

    @property
    def kind(self):
        return ExprASTKind.TensorLiteral
    
"""
MULTIPLICATION:
(set C (matmul A B))
ADDITION:
(set C (+ A B))
"""  
@dataclass
class TensorOpExprAST(ExprAST):
    op: str  # Operation type, e.g., "matmul" or "+"
    lhs: ExprAST  # Left-hand side tensor expression
    rhs: ExprAST  # Right-hand side tensor expression

    @property
    def kind(self):
        return ExprASTKind.TensorOp