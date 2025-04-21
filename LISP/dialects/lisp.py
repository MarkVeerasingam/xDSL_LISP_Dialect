from typing import Annotated
from xdsl.context import Context
from xdsl.printer import Printer
from xdsl.ir import Dialect, OpResult
from xdsl.dialects.arith import ConstantOp, SignlessIntegerBinaryOperation
from xdsl.irdl import (
    Operand, 
    operand_def, 
    result_def,
    IRDLOperation,
    irdl_op_definition,
    register
)
from xdsl.dialects.builtin import (
    i64,
    i32
)


class LispDialect(Dialect):
    name = "lisp"

    context = Context()

    context.load_dialect(ConstantOp)

#     context.register_dialect(LispAddOp)
