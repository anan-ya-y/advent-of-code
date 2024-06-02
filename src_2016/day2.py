import numpy as np
import utils
grid = np.arange(1, 10).reshape((3, 3))
grid2 = ["xx1xx", "x234x", "56789", "xABCx", "xxDxx"]

def move(pos, c, gridsize):
    if c == 'U':
        pos = (max(0, pos[0]-1), pos[1])
    elif c == 'D':
        pos = (min(gridsize-1, pos[0]+1), pos[1])
    elif c == 'L':
        pos = (pos[0], max(0, pos[1]-1))
    elif c == 'R':
        pos = (pos[0], min(gridsize-1, pos[1]+1))
    return pos


def p1(input):
    input = utils.split_and_strip(input)

    pos = (1, 1)
    ans = ""
    for line in input:
        for c in line:
            pos = move(pos, c, 3)
        ans += str(grid[pos])
    return ans
    
def p2(input):
    input = utils.split_and_strip(input)
    pos = (2, 0)
    ans = ""

    for line in input:
        for c in line:
            newpos = move(pos, c, 5)
            if grid2[newpos[0]][newpos[1]] != "x":
                pos = newpos
        ans += str(grid2[pos[0]][pos[1]])
    return ans