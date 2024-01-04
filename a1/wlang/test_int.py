# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from . import ast, int, mockVisitor


class TestInt(unittest.TestCase):
    def test_one(self):
        prg1 = "x := 10; print_state"
        # test parser
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)
        # x is defined
        self.assertIn("x", st.env)
        # x is 10
        self.assertEquals(st.env["x"], 10)
        # no other variables in the state
        self.assertEquals(len(st.env), 1)

    def test_if_statement(self):
        prg1 = "x := -3; if x > 10 then x := 10 else x := 20; print_state"
        prg2 = "x := -3; if x > 10 then x := 10 else x := 20; print_state"
        ast1 = ast.parse_string(prg1)
        ast2 = ast.parse_string(prg2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEqual(ast1, ast2)
        self.assertIsNotNone(st)
        # x is defined
        self.assertIn("x", st.env)
        # x is 20
        self.assertEquals(st.env["x"], 20)
        # no other variables in the state
        self.assertEquals(len(st.env), 1)

    def test_while_statement(self):
        prg1 = "x := 0; while x < 10 inv false do x := x + 1; print_state"
        prg2 = "x := 0; while x < 10 inv false do x := x + 1; print_state"
        ast1 = ast.parse_string(prg1)
        ast2 = ast.parse_string(prg2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEqual(ast1, ast2)
        self.assertIsNotNone(st)
        # x is defined
        self.assertIn("x", st.env)
        # x is 10
        self.assertEquals(st.env["x"], 10)
        # no other variables in the state
        self.assertEquals(len(st.env), 1) 
    
    def test_assert_statement(self):
        prg1 = "x := 10; assert (x > 0); print_state"
        prg2 = "x := 10; assert (x > 0); print_state"
        ast1 = ast.parse_string(prg1)
        ast2 = ast.parse_string(prg2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEqual(ast1, ast2)
        # x is defined
        self.assertIn("x", st.env)
        # x is 10
        self.assertEquals(st.env["x"], 10)
        # no other variables in the state
        self.assertEquals(len(st.env), 1) 

    def test_assume_statement(self):
        prg1 = "x := 10; assume (x > 0); skip"
        prg2 = "x := 10; assume (x > 0); skip"
        ast1 = ast.parse_string(prg1)
        ast2 = ast.parse_string(prg2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEqual(ast1, ast2)
        # x is defined
        self.assertIn("x", st.env)
        # x is 10
        self.assertEquals(st.env["x"], 10)
        # no other variables in the state
        self.assertEquals(len(st.env), 1) 

    def test_havoc_statement(self):
        prg1 = "havoc x, y; print_state"
        prg2 = "havoc x, y; print_state"
        ast1 = ast.parse_string(prg1)
        ast2 = ast.parse_string(prg2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEqual(ast1, ast2)
        # x, y is defined
        self.assertIn("x", st.env)
        self.assertIn("y", st.env)
        # no other variables in the state
        self.assertEquals(len(st.env), 2)

    def test_bool_const(self):
        prg1 = "if true and false then skip else print_state"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEquals(len(st.env), 0)

    def test_relexp(self):
        prg1 = "if 1 <= 2 and 4 >= 3 then skip else print_state"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEquals(len(st.env), 0)

    def test_bexp(self):
        prg1 = "if not true or 1 = 1 then skip"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEquals(len(st.env), 0)

    def test_aexp(self):
        prg1 = "x := 1; y := x * (4 - 2) / -1; print_state"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
         # x, y is defined
        self.assertIn("x", st.env)
        self.assertIn("y", st.env)
         # x is 1, y is -2
        self.assertEquals(st.env["x"], 1)
        self.assertEquals(st.env["y"], -2)
        # no other variables in the state
        self.assertEquals(len(st.env), 2)

    # def test_assertError(self):

    def test_one_statement(self):
        prg1 = "{x := 10}"
        # test parser
        ast1 = ast.parse_string(prg1)
        print(ast1)
        print(repr(ast1))
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)

    def test_empty_statement(self):
        prg1 = "x := 10"
        ast1 = ast.parse_string(prg1)
        
        print(ast1)
        print(repr(ast1))
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)

    def test_bexp2(self):
        prg1 = "x := 3; if x <= 4 and x >= 1 then skip else print_state"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
         # x is defined
        self.assertIn("x", st.env)
         # x is 1
        self.assertEquals(st.env["x"], 3)
        # no other variables in the state
        self.assertEquals(len(st.env), 1)

    def test_multiple_operators(self):
        exp = ast.Exp(["+", "*"], [1, 2])
        self.assertTrue(exp.is_binary())

    def test_parse_file(self):
        ast1 = ast.parse_file("wlang/test1.prg")
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
         # x is defined
        self.assertIn("x", st.env)
         # x is 1
        self.assertEquals(st.env["x"],10)
        # no other variables in the state
        self.assertEquals(len(st.env), 1)

    def test_mock_if_visitor(self):
        prg1 = "z := 2; if z = 1 then skip"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)

    def test_mock_while_visitor(self):
        prg1 = "z := 2; while z > 0 do print_state"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)

    def test_mock_skip_visitor(self):
        prg1 = "skip"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)

    def test_mock_print_visitor(self):
        prg1 = "print_state"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)
    
    def test_mock_assume_visitor(self):
        prg1 = "x := 1; assume x > 0"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)

    def test_mock_assert_visitor(self):
        prg1 = "x := 1; assert x > 0"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)

    def test_mock_havoc_visitor(self):
        prg1 = "havoc x"
        ast1 = ast.parse_string(prg1)
        visitor = mockVisitor.StmtVisitorMock()
        visitor.visit(ast1)

    def test_int_var(self):
        var = ast.IntVar("x")
        print(var)
        print(repr(var))
        mydict = {}
        mydict[var] = 1

    def test_const(self):
        var = ast.Const(1)
        print(var)
        print(repr(var))
        mydict = {}
        mydict[var] = 1

    def test_print_visitor(self):
        prg1 = "havoc x"
        ast1 = ast.parse_string(prg1)
        ast1.stmts = None
        print_visitor = ast.PrintVisitor(None)
        print_visitor.visit_StmtList(ast1)

    def test_if_false_path(self):
        prg1 = "if false then skip"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(ast1)
        print(repr(ast1))
        self.assertEquals(len(st.env), 0)

    def test_assert_false_path(self):
        with self.assertRaises(AssertionError):
            prg1 = "x := 1; \n assert x < 0\n"
            ast1 = ast.parse_string(prg1)
            interp = int.Interpreter()
            st = int.State()
            st.__repr__()
            st = interp.run(ast1, st)
            print(ast1)
            print(repr(ast1))
            # x is defined
            self.assertIn("x", st.env)
            # x is 1
            self.assertEquals(st.env["x"],1)
            # no other variables in the state
            self.assertEquals(len(st.env), 1)
