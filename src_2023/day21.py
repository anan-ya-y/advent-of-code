import utils
import numpy.linalg as la
import numpy as np
C = complex

NORTH = C(-1, 0)
SOUTH = C(1, 0)
EAST = C(0, 1)
WEST = C(0, -1)

directions = [NORTH, EAST, SOUTH, WEST]

def get_positions(input):
    invalid_pos = set()
    start = -1
    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] == "#":
                invalid_pos.add(C(r, c))
            if input[r][c] == "S":
                start = C(r, c)

    return invalid_pos, start, len(input), len(input[0])

def get_next_positions(invalid_pos, pos, nrows=-1, ncols=-1):
    new_pos = set()
    for p in pos:
        for d in directions:
            new = p+d
            if nrows > 0 and ncols > 0:
                new_compare = C(new.real % nrows, new.imag % ncols)
            else:
                new_compare = new

            if new_compare not in invalid_pos:
                new_pos.add(new)
    return new_pos

def p1(input):
    input = utils.split_and_strip(input)
    invalid, start, _, _ = get_positions(input)

    nsteps = 64
    pos = set([start])
    for _ in range(nsteps):
        pos = get_next_positions(invalid, pos)
    return len(pos)

     

def p2(input):
    input = utils.split_and_strip(input)
    invalid, start, nrows, ncols = get_positions(input)

    # thank you reddit
    # the number of positions can be found by using a quadratic fmla
    # why? I do not know. something something squares, triangles, and a diamond
    # 26501365 is the 100th triangle number according to chatgpt

    nsteps = 26501365
    remainder = nsteps % nrows
    #f(x) = number of positions after nrows*x + remainder steps
    # get the pattern
    pos = set([start])
    function_y_vals = []
    for i in range(nrows * 2 + remainder + 1):
        if i % nrows == remainder:
            function_y_vals.append(len(pos))
        pos = get_next_positions(invalid, pos, nrows, ncols)
        # print(i, len(pos))
          
    # soln = np.polynomial.polynomial.polyfit([0,1,2],function_y_vals,2)
    print(function_y_vals)
    soln = la.lstsq(np.array([[1, 0, 0], [1,1, 1], [1, 2,4]]), \
                    np.array(function_y_vals))[0]
    soln = np.round(soln, 0)
    print(soln)
    x = (nsteps // nrows)
    return int(np.dot(np.array([1, x, x**2]), soln))