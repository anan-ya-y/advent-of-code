import utils, re

def is_triangle(sides):
    sides.sort()
    return sides[2] < sides[0] + sides[1]

def p1(input):
    input = utils.split_and_strip(input)
    ans = 0
    for line in input:
        sides = utils.split_by_whitespace(line)
        sides = list(map(int, sides))
        ans += is_triangle(sides)
    return ans

def p2(input):
    input = utils.split_and_strip(input)
    ans = 0
   
    for i in range(0, len(input), 3):
        lines = input[i:i+3]
        lines = [utils.split_by_whitespace(l) for l in lines]
        lines = [list(map(int, l)) for l in lines]
        for i in range(3):
            ans += is_triangle([lines[0][i], lines[1][i], lines[2][i]])

    return ans