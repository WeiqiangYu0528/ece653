import unittest

from . import ast, undef_visitor


class TestUndefVisitor(unittest.TestCase):
    def test1(self):
        prg1 = "x := 10; y := x + z"
        ast1 = ast.parse_string(prg1)

        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('z')]), uv.get_undefs ())

    def testAssume(self):
        prg1 = "assume x > 0"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('x')]), uv.get_undefs ())

    def testAssert(self):
        prg1 = "assert x > 0"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('x')]), uv.get_undefs ())

    def testHavoc(self):
        prg1 = "havoc x, y, z; b := a + x + y + z"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('a')]), uv.get_undefs ())

    def testIf(self):
        prg1 = "x := 10; if x < 0 then y := 1 else z := 2; z := x + y + z"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('y'), ast.IntVar('z')]), uv.get_undefs ())

    def testWhile(self):
        prg1 = "x := 5; while y > 0 do {z := x + 3; skip}; y := z - 1"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('y'), ast.IntVar('z')]), uv.get_undefs ())

    def testIfTwo(self):
        prg1 = "x := 10; if x < 0 then y := 1; z := y + x"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('y')]), uv.get_undefs ())

    def testIfThree(self):
        prg1 = "havoc x; if x > 10 then y := x + 1 else z := 10; x := z + 1"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('z')]), uv.get_undefs ())
    
