'''Magic Square

https://en.wikipedia.org/wiki/Magic_square

A magic square is a n * n square grid filled with distinct positive integers in
the range 1, 2, ..., n^2 such that each cell contains a different integer and
the sum of the integers in each row, column, and diagonal is equal.

'''

from z3 import Solver, sat, unsat, FreshInt, Distinct


def solve_magic_square(n, r, c, val):
    solver = Solver()
    cond = []
    nums = [[0] * n for _ in range(n)]
    sum_ = (1 + n * n) * (n * n) / (2 * n)
    for i in range(n):
        row_ = 0
        for j in range(n):
            nums[i][j] = FreshInt('x')
            cond.append(1 <= nums[i][j])
            cond.append(nums[i][j] <= n * n)
            row_ += nums[i][j]
        cond.append(row_ == sum_)

    for j in range(n):
        col_ = 0
        for i in range(n):
            col_ += nums[i][j]
        cond.append(col_ == sum_)

    diagonal1 = 0
    diagonal2 = 0
    for i in range(n):
        diagonal1 += nums[i][i]
        diagonal2 += nums[i][n - i - 1]
    cond.append(diagonal1 == sum_)
    cond.append(diagonal2 == sum_)
    
    cond.append(nums[r][c] == val)

    solver.add(Distinct([nums[i][j] for i in range(n) for j in range(n)]))
    solver.add(cond)

    # CREATE CONSTRAINTS AND LOAD STORE THEM IN THE SOLVER

    if solver.check() == sat:
        mod = solver.model()
        res = [[0] * n for _ in range(n)]

        # CREATE RESULT MAGIC SQUARE BASED ON THE MODEL FROM THE SOLVER
        for i in range(n):
            for j in range(n):
                res[i][j] = mod.eval(nums[i][j]).as_long()

        # print_square(res)
        return res
    else:
        return None


def print_square(square):
    '''
    Prints a magic square as a square on the console
    '''
    n = len(square)

    assert n > 0
    for i in range(n):
        assert len(square[i]) == n

    for i in range(n):
        line = []
        for j in range(n):
            line.append(str(square[i][j]))
        print('\t'.join(line))


def puzzle(n, r, c, val):
    res = solve_magic_square(n, r, c, val)
    if res is None:
        print('No solution!')
    else:
        print('Solution:')
        print_square(res)


if __name__ == '__main__':
    n = 3
    r = 1
    c = 1
    val = 5
    puzzle(n, r, c, val)
