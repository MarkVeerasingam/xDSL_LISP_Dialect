from LISP.frontend.lexer import LispLexer
from LISP.frontend.lisp_ast import *
from LISP.frontend.parser import LispParser
import unittest

class TestLispParser(unittest.TestCase):
    def setUp(self):
        self.file_name = "<test_file>"

    def test_var_decl(self):
        # Test parsing a simple variable declaration: (set x 5)
        code = "(set x 5)"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)
        
        ast = parser.parse()
        
        # Check that the AST root is of type VarDeclExprAST
        self.assertIsInstance(ast, VarDeclExprAST)
        
        # Check that the name of the variable is 'x'
        self.assertEqual(ast.name, "x")
        
        # Check that the value of the expression is a NumberExprAST with value 5
        self.assertIsInstance(ast.expr, NumberExprAST)
        self.assertEqual(ast.expr.val, 5)

    def test_binary_expr(self):
        # Test parsing a binary expression: (+ x 2)
        code = "(+ x 2)"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)
        
        ast = parser.parse()
        
        # Check that the AST root is of type BinaryExprAST
        self.assertIsInstance(ast, BinaryExprAST)
        
        # Check the operator is '+'
        self.assertEqual(ast.op, "+")
        
        # Check the left-hand side is a variable 'x'
        self.assertIsInstance(ast.lhs, VariableExprAST)
        self.assertEqual(ast.lhs.name, "x")
        
        # Check the right-hand side is a number 2
        self.assertIsInstance(ast.rhs, NumberExprAST)
        self.assertEqual(ast.rhs.val, 2)

    def test_return_stmt(self):
        # Test parsing a return statement: (return x)
        code = "(return x)"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)
        
        ast = parser.parse()
        
        # Check that the AST root is of type ReturnExprAST
        self.assertIsInstance(ast, ReturnExprAST)
        
        # Check that the returned expression is a variable 'x'
        self.assertIsInstance(ast.expr, VariableExprAST)
        self.assertEqual(ast.expr.name, "x")

    def test_nested_expr(self):
        # Test parsing a nested expression: (set x (+ 2 3))
        code = "(set x (+ 2 3))"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)
        
        ast = parser.parse()
        
        # Check that the AST root is of type VarDeclExprAST
        self.assertIsInstance(ast, VarDeclExprAST)
        
        # Check the expression inside the var declaration is a BinaryExprAST
        self.assertIsInstance(ast.expr, BinaryExprAST)
        
        # Check that the operator is '+'
        self.assertEqual(ast.expr.op, "+")
        
        # Check the left-hand side of the binary expression is a number 2
        self.assertIsInstance(ast.expr.lhs, NumberExprAST)
        self.assertEqual(ast.expr.lhs.val, 2)
        
        # Check the right-hand side of the binary expression is a number 3
        self.assertIsInstance(ast.expr.rhs, NumberExprAST)
        self.assertEqual(ast.expr.rhs.val, 3)

    def test_tensor_literal(self):
        # Test parsing a tensor literal: [[1 2] [3 4]]
        code = "([[1 2] [3 4]])"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)

        ast = parser.parse()
        self.assertIsInstance(ast, TensorLiteralExprAST)

        self.assertEqual(ast.elements, [[1.0, 2.0], [3.0, 4.0]])
        self.assertEqual(ast.tensor_type.shape, [2, 2])

    def test_tensor_var_decl(self):
        # Test parsing tensor assignment to variable
        code = "(set A ([[1 2] [3 4]]))"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)

        ast = parser.parse()
        self.assertIsInstance(ast, VarDeclExprAST)
        self.assertEqual(ast.name, "A")
        self.assertIsInstance(ast.expr, TensorLiteralExprAST)
        self.assertEqual(ast.expr.elements, [[1.0, 2.0], [3.0, 4.0]])

    def test_tensor_op_matmul(self):
        # Test tensor operation: (matmul A B)
        code = "(matmul A B)"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)

        ast = parser.parse()
        self.assertIsInstance(ast, TensorOpExprAST)
        self.assertEqual(ast.op, "matmul")
        self.assertIsInstance(ast.lhs, VariableExprAST)
        self.assertEqual(ast.lhs.name, "A")
        self.assertIsInstance(ast.rhs, VariableExprAST)
        self.assertEqual(ast.rhs.name, "B")

    def test_tensor_op_add(self):
        # Test binary op addition on tensors: (+ A B)
        code = "(+ A B)"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)

        ast = parser.parse()
        self.assertIsInstance(ast, BinaryExprAST)
        self.assertEqual(ast.op, "+")
        self.assertIsInstance(ast.lhs, VariableExprAST)
        self.assertEqual(ast.lhs.name, "A")
        self.assertIsInstance(ast.rhs, VariableExprAST)
        self.assertEqual(ast.rhs.name, "B")

    def test_paren_wrapped_number(self):
        code = "(5)"
        lexer = LispLexer(code)
        parser = LispParser(lexer, self.file_name)

        ast = parser.parse()
        self.assertIsInstance(ast, NumberExprAST)
        self.assertEqual(ast.val, 5)

if __name__ == "__main__":
    unittest.main()