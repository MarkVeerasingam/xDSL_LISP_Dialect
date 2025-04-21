from .lisp_ast import *
from .lexer import LispLexer, LispTokenKind
from .location import Location

class LispParser:
    def __init__(self, lexer: LispLexer, file_name: str = "<stdin>"):
        self.tokens = list(lexer)
        self.index = 0
        self.file_name = file_name

    def current_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return None

    def eat(self, expected_type: str):
        tok = self.current_token()
        if tok is None:
            raise SyntaxError("Unexpected end of input")
        if tok.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {tok.type}")
        self.index += 1
        return tok

    def parse(self) -> ExprAST:
        tok = self.current_token()
        if tok.type == "PARENTHESE_OPEN":
            return self.parse_expr()
        else:
            raise SyntaxError(f"Unexpected token {tok.type}")

    def parse_expr(self) -> ExprAST:
        self.eat("PARENTHESE_OPEN")
        tok = self.current_token()

        if tok.type == "SET":
            return self.parse_var_decl()
        elif tok.type == "RETURN":
            return self.parse_return()
        elif tok.type == "OPERATOR":
            return self.parse_binary()
        elif tok.type == "TENSOR_OP":
            return self.parse_tensor_op()
        else:
            expr = self.parse_any_expr()
            self.eat("PARENTHESE_CLOSE")
            return expr

    def parse_var_decl(self) -> VarDeclExprAST:
        set_tok = self.eat("SET")
        name_tok = self.eat("IDENTIFIER")
        expr = self.parse_any_expr()
        self.eat("PARENTHESE_CLOSE")
        return VarDeclExprAST(
            loc=self.get_loc(set_tok),
            name=name_tok.value,
            var_type=VarType([]),
            expr=expr
        )

    def parse_return(self) -> ReturnExprAST:
        ret_tok = self.eat("RETURN")
        expr = self.parse_any_expr()
        self.eat("PARENTHESE_CLOSE")
        return ReturnExprAST(loc=self.get_loc(ret_tok), expr=expr)

    def parse_binary(self) -> BinaryExprAST:
        op_tok = self.eat("OPERATOR")
        lhs = self.parse_any_expr()
        rhs = self.parse_any_expr()
        self.eat("PARENTHESE_CLOSE")
        return BinaryExprAST(
            loc=self.get_loc(op_tok),
            op=op_tok.value,
            lhs=lhs,
            rhs=rhs
        )

    def parse_any_expr(self) -> ExprAST:
        tok = self.current_token()
        if tok.type == "NUMBER":
            num_tok = self.eat("NUMBER")
            return NumberExprAST(loc=self.get_loc(num_tok), val=float(num_tok.value))
        elif tok.type == "IDENTIFIER":
            id_tok = self.eat("IDENTIFIER")
            return VariableExprAST(loc=self.get_loc(id_tok), name=id_tok.value)
        elif tok.type == "PARENTHESE_OPEN":
            return self.parse_expr()
        elif tok.type == "SQUARE_BRACKET_OPEN":
            return self.parse_tensor_literal()
        else:
            raise SyntaxError(f"Unexpected token {tok.type} in expression")
        
    def parse_tensor_literal(self) -> TensorLiteralExprAST:
        elements = []
        self.eat("SQUARE_BRACKET_OPEN")

        while self.current_token().type == "SQUARE_BRACKET_OPEN":
            row = []
            self.eat("SQUARE_BRACKET_OPEN")
            while self.current_token().type == "NUMBER":
                num_tok = self.eat("NUMBER")
                row.append(float(num_tok.value))
            self.eat("SQUARE_BRACKET_CLOSE")
            elements.append(row)

        self.eat("SQUARE_BRACKET_CLOSE")
        shape = [len(elements), len(elements[0]) if elements else 0]
        tensor_type = TensorVarType(shape=shape)
        return TensorLiteralExprAST(loc=self.get_loc(self.current_token()), elements=elements, tensor_type=tensor_type)
    
    def parse_tensor_op(self) -> TensorOpExprAST:
        op_tok = self.eat("TENSOR_OP")
        lhs = self.parse_any_expr()
        rhs = self.parse_any_expr()
        self.eat("PARENTHESE_CLOSE")
        return TensorOpExprAST(
            loc=self.get_loc(op_tok),
            op=op_tok.value,
            lhs=lhs,
            rhs=rhs
        )

    def get_loc(self, token):
        # Simplified: might want to integrate actual location tracking
        return Location(file=self.file_name, line=1, col=1)
