import utils
import re
import z3

C = complex

def manhattan(x, y):
    return abs(x.real - y.real) + abs(x.imag - y.imag)

def get_circle_intersections(s, b, y):
    radius = manhattan(s, b)

    dist = abs(s.imag - y)
    if dist > radius:
        return set()
    pm = (radius - dist)
    ints = set(range(int(s.real-pm), int(s.real+pm+1)))
    if b.imag == y:
        ints.remove(b.real)

    return ints

def read_input(input):
    lines = utils.split_and_strip(input)
    sb = {}
    for l in lines:
        nums = list(map(int, re.findall(r"(-?\d+)", l)))
        sb[C(nums[0], nums[1])] = C(nums[2], nums[3])
    return sb

def p1(input):
    sb = read_input(input)
    lineNum = 2000000

    impossible_positions = set()

    for s in sb:
        b = sb[s]
        ints = get_circle_intersections(s, b, lineNum)
        impossible_positions = impossible_positions.union(ints)

    return len(impossible_positions)

# we can do p2 my way, and yes it works (at ~4s/row) but z3 gooder
def p2(input):
    sb = read_input(input)

    x = z3.Int('x')
    y = z3.Int('y')
    solver = z3.Solver()

    solver.add(x >= 0)
    solver.add(y >= 0)
    solver.add(x <= 4000000)
    solver.add(y <= 4000000)

    def z3abs(x):
        return z3.If(x >= 0,x,-x)
    
    for s in sb:
        b = sb[s]
        solver.add(manhattan(s, b) < z3abs(s.real - x) + z3abs(s.imag - y))
    
    solver.check()
    model = solver.model()
    return (model[x].as_long() * 4000000 + model[y].as_long())
        