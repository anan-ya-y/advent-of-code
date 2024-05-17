import utils

def p1(input):
    input = utils.split_lines(input)
    total = 0
    for line in input:
        x, y, z = map(int, line.split('x'))
        sides = [x*y, y*z, z*x]
        total += 2*sum(sides) + min(sides)
    return total

def p2(input):
    input = utils.split_lines(input)
    total = 0
    for line in input:
        vals = list(map(int, line.split('x')))
        vals.sort()

        total += 2*(vals[0]+vals[1])
        total += vals[0]*vals[1]*vals[2]
    return total