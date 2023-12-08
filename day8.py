import utils
import re
import math

def get_endpt(startpos, desertmap, directions):
    if directions == "":
        return startpos
    if directions[0] == "L":
        next_loc = desertmap[startpos][0]
    else:
        next_loc = desertmap[startpos][1]
    return get_endpt(next_loc, desertmap, directions[1:])

def get_nsteps(startpos, desertmap, directions):
    pos = startpos
    nsteps = 0
    while pos[-1] != "Z":
        pos = get_endpt(pos, desertmap, directions)
        nsteps += len(directions)
    return nsteps

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def p1(input):
    lines = input.split("\n\n")
    directions = lines[0].strip()

    maplines = [re.findall(r"(\w+) = \((\w+), (\w+)\)", l)[0] for l in lines[1].split("\n")]

    desertmap = dict((i, (j, k)) for i, j, k in maplines)
    
    return get_nsteps("AAA", desertmap, directions)
    

def p2(input):
    lines = input.split("\n\n")
    directions = lines[0].strip()

    maplines = [re.findall(r"(\w+) = \((\w+), (\w+)\)", l)[0] for l in lines[1].split("\n")]

    desertmap = dict((i, (j, k)) for i, j, k in maplines)
    
    startpostitions = [d for d in desertmap if d[-1] == "A"]
    nsteps = [get_nsteps(d, desertmap, directions) for d in startpostitions]
    minsteps_all = nsteps[0]
    for n in nsteps[1:]:
        minsteps_all = lcm(minsteps_all, n)
    return minsteps_all


