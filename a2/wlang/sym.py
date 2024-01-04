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

import sys

import io 
import z3
from functools import reduce

from . import ast, int


class SymState(object):
    def __init__(self, solver=None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver()

        # true if this is an error state
        self._is_error = False

    def add_pc(self, *exp):
        """Add constraints to the path condition"""
        self.path.extend(exp)
        self._solver.append(exp)

    def is_error(self):
        return self._is_error

    def mk_error(self):
        self._is_error = True

    def is_empty(self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check()
        return res == z3.unsat

    def pick_concerete(self):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""
        res = self._solver.check()
        if res != z3.sat:
            return None
        model = self._solver.model()
        st = int.State()
        for (k, v) in self.env.items():
            st.env[k] = model.eval(v)
        return st

    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState()
        child.env = dict(self.env)
        child.add_pc(*self.path)

        return (self, child)

    def __repr__(self):
        return str(self)

    def to_smt2(self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2()

    def __str__(self):
        buf = io.StringIO()
        for k, v in self.env.items():
            buf.write(str(k))
            buf.write(': ')
            buf.write(str(v))
            buf.write('\n')
        buf.write('pc: ')
        buf.write(str(self.path))
        buf.write('\n')

        return buf.getvalue()


class SymExec(ast.AstVisitor):
    def __init__(self):
        pass

    def run(self, ast, state):
        # set things up and
        # call self.visit (ast, state=state)
        states = [state]
        return self.visit(ast, states=states)

    def visit_IntVar(self, node, *args, **kwargs):
        return kwargs['states'].env[node.name]

    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal(node.val)

    def visit_IntConst(self, node, *args, **kwargs):
        return z3.IntVal(node.val)

    def visit_RelExp(self, node, *args, **kwargs):
        lhs = self.visit(node.arg(0), *args, **kwargs)
        rhs = self.visit(node.arg(1), *args, **kwargs)
        if node.op == "<=":
            return lhs <= rhs
        if node.op == "<":
            return lhs < rhs
        if node.op == "=":
            return lhs == rhs
        if node.op == ">=":
            return lhs >= rhs
        if node.op == ">":
            return lhs > rhs

    def visit_BExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        if node.op == "not":
            assert node.is_unary()
            assert len(kids) == 1
            return z3.Not(kids[0])

        fn = None
        base = None
        if node.op == "and":
            fn = lambda x, y: z3.And(x, y)
            base = True
        elif node.op == "or":
            fn = lambda x, y: z3.Or(x, y)
            base = False

        assert fn is not None
        return reduce(fn, kids, base)

    def visit_AExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        fn = None

        if node.op == "+":
            fn = lambda x, y: x + y

        elif node.op == "-":
            fn = lambda x, y: x - y

        elif node.op == "*":
            fn = lambda x, y: x * y

        elif node.op == "/":
            fn = lambda x, y: x / y

        assert fn is not None
        return reduce(fn, kids)

    def visit_SkipStmt(self, node, *args, **kwargs):
        return kwargs["states"]

    def visit_PrintStateStmt(self, node, *args, **kwargs):
        print(kwargs["states"])
        return kwargs["states"]

    def visit_AsgnStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        nkwargs = dict(kwargs)
        for st in states:
            nkwargs['states'] = st
            st.env[node.lhs.name] = self.visit(node.rhs, *args, **nkwargs)
        return states

    def visit_IfStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        res, res1, res2 = [], [], []
        nkwargs = dict(kwargs)
        for st in states:
            nkwargs["states"] = st
            cond = self.visit(node.cond, *args, **nkwargs)
            s1, s2 = st.fork()
            s1.add_pc(cond)
            s2.add_pc(z3.Not(cond))
            if not s1.is_empty():
                res1.append(s1)
            if not s2.is_empty():
                res2.append(s2)
            
        if len(res1) > 0:
            nkwargs["states"] = res1
            res.extend(self.visit(node.then_stmt, *args, **nkwargs))

        if len(res2) > 0:
            if node.has_else():
                nkwargs["states"] = res2
                res.extend(self.visit(node.else_stmt, *args, **nkwargs))
            else:
                res.extend(res2)

        return res

    def visit_WhileStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        nkwargs = dict(kwargs)
        res = []
        for i in range(11):
            res1, res2 = [], []
            for st in states:
                nkwargs["states"] = st
                cond = self.visit(node.cond, *args, **nkwargs)
                s1, s2 = st.fork()
                s1.add_pc(cond)
                s2.add_pc(z3.Not(cond))
                if not s1.is_empty():
                    res1.append(s1)
                if not s2.is_empty():
                    res2.append(s2)
            
            res.extend(res2)
            if len(res1) == 0:
                break
            nkwargs["states"] = res1
            states = self.visit(node.body, *args, **nkwargs)

        return res

    def visit_AssertStmt(self, node, *args, **kwargs):
        # Don't forget to print an error message if an assertion might be violated
        states = kwargs["states"]
        res = []
        nkwargs = dict(kwargs)
        for st in states:
            nkwargs["states"] = st
            cond = self.visit(node.cond, *args, **nkwargs)
            s1, s2 = st.fork()
            s1.add_pc(z3.Not(cond))
            s2.add_pc(cond)
            if not s1.is_empty():
                s1.mk_error()
                s1.is_error()
                print("Assertion might be violated")
            if not s2.is_empty():
                res.append(s2)
        return res

    def visit_AssumeStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        res = []
        nkwargs = dict(kwargs)
        for st in states:
            nkwargs["states"] = st
            cond = self.visit(node.cond, *args, **nkwargs)
            st.add_pc(cond)
            if not st.is_empty():
                res.append(st)
            else:
                st.pick_concerete()
        return res

    def visit_HavocStmt(self, node, *args, **kwargs):
        states = kwargs["states"]
        for st in states:
            for v in node.vars:
                # assign 0 as the default value
                st.env[v.name] = z3.FreshInt(v.name)
        return states

    def visit_StmtList(self, node, *args, **kwargs):
        st = kwargs["states"]
        nkwargs = dict(kwargs)
        for stmt in node.stmts:
            nkwargs["states"] = st
            st = self.visit(stmt, *args, **nkwargs)
            # print(st)
        return st

def _parse_args():
    import argparse
    ap = argparse.ArgumentParser(prog='sym',
                                 description='WLang Interpreter')
    ap.add_argument('in_file', metavar='FILE',
                    help='WLang program to interpret')
    args = ap.parse_args()
    return args


def main():
    args = _parse_args()
    prg = ast.parse_file(args.in_file)
    st = SymState()
    sym = SymExec()

    states = sym.run(prg, st)
    if states is None:
        print('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print('[symexec]: symbolic state reached')
            print(out)
        print('[symexec]: found', count, 'symbolic states')
    return 0


if __name__ == '__main__':
    sys.exit(main())