"""
list_ast.py
this file defines the abstract syntax tree (ast) of our LISP style language.
Each node in the AST corresponds to a syntactic construct in the language.
"""

from __future__ import annotations

from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass
from enum import Enum

from .location import Location

INDENT = 2

@dataclass
class VarType:
    "A variable type with shape information. e.g a matrix dimension"
    # shape: list[int]
    "For simplicity, we will just keep it basic for now. Will add lists/matrices in later"
    shape: int

class ExprASTKind(Enum):
    Expr_VarDecl = 1     # "(set x 5)"
    Expr_Return = 2     # "(return x)"
    Expr_Num = 3        # "10"
    Expr_Var = 4        # "x"
    Expr_BinOp = 5      # "(+ x 2)"
    # add later:
    # Expr_Print = 6    # "(print x)"

@dataclass()
class Dumper:
    lines: list[str]
    indentation: int = 0

    def append(self, prefix: str, line: str):
        """ Append a line with the given indentation """
        self.lines.append(" " * self.indentation * INDENT + prefix + line)

    def append_list(
        self,
        prefix: str,
        open_paren: str,
        exprs: Iterable[ExprAST],
        close_paren: str,
        block: Callable[[Dumper, ExprAST], None],
    ):
        """ Helper for appending a list of expressions """
        self.append(prefix, open_paren)
        child = self.child()
        for expr in exprs:
            block(child, expr)
        self.append("", close_paren)

    def child(self):
        """ Create a child Dumper instance with increased indentation """
        return Dumper(self.lines, self.indentation + 1)

    @property
    def message(self):
        """ Return the formatted lines as a single string """
        return "\n".join(self.lines)

@dataclass
class ExprAST:
    loc: Location

    def __init__(self, loc: Location):
        self.loc = loc
        print(self.dump())

    @property
    def kind(self) -> ExprASTKind:
        raise AssertionError(f"ExprAST kind not defined for {type(self)}")

    def inner_dump(self, prefix: str, dumper: Dumper):
        dumper.append(prefix, self.__class__.__name__)

    def dump(self):
        dumper = Dumper([])
        self.inner_dump("", dumper)
        return dumper.message

@dataclass
class VarDeclExprAST(ExprAST):
    "Expression class for defining a variable."

    name: str
    varType: VarType
    expr: ExprAST

    @property
    def kind(self):
        return ExprASTKind.Expr_VarDecl

    def inner_dump(self, prefix: str, dumper: Dumper):
        dims_str = ", ".join(f"{int(dim)}" for dim in self.varType.shape)
        dumper.append("VarDecl ", f"{self.name}<{dims_str}> @{self.loc}")
        child = dumper.child()
        self.expr.inner_dump("", child)

@dataclass
class NumberExprAST(ExprAST):
    'Expression class for numeric literals like "1.0".'

    val: float

    @property
    def kind(self):
        return ExprASTKind.Expr_Num

    def inner_dump(self, prefix: str, dumper: Dumper):
        dumper.append(prefix, f" {self.val:.6e}")

@dataclass
class VariableExprAST(ExprAST):
    'Expression class for referencing a variable, like "a".'

    name: str

    @property
    def kind(self):
        return ExprASTKind.Expr_Var

    def inner_dump(self, prefix: str, dumper: Dumper):
        dumper.append("var: ", f"{self.name} @{self.loc}")

@dataclass
class BinaryExprAST(ExprAST):
    "Expression class for a binary operator."

    op: str
    lhs: ExprAST
    rhs: ExprAST

    @property
    def kind(self):
        return ExprASTKind.Expr_BinOp

    def inner_dump(self, prefix: str, dumper: Dumper):
        dumper.append(prefix, f"BinOp: {self.op} @{self.loc}")
        child = dumper.child()
        self.lhs.inner_dump("", child)
        self.rhs.inner_dump("", child)

@dataclass
class ReturnExprAST(ExprAST):
    "Expression class for a return statement."

    expr: ExprAST  # The expression to return, if any.

    @property
    def kind(self):
        return ExprASTKind.Expr_Return

    def inner_dump(self, prefix: str, dumper: Dumper):
        dumper.append(prefix, "Return")
        child = dumper.child()
        self.expr.inner_dump("", child)
