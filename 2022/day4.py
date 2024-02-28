import utils
import re

def does_intersect(c1, c2):
    return (c1[0] >= c2[0] and c1[1] <= c2[1]) \
        or (c1[0] <= c2[0] and c1[1] >= c2[1]) 

def p1(input):
    lines = utils.split_and_strip(input)

    nintersect = 0
    for line in lines:
        x = re.findall(r'(\d+)-(\d+),(\d+)-(\d+)', line)
        c1 = (int(x[0][0]), int(x[0][1]))
        c2 = (int(x[0][2]), int(x[0][3]))

        if does_intersect(c1, c2):
            nintersect += 1
    return nintersect

def p2(input):
    lines = utils.split_and_strip(input)

    nintersect = 0
    for line in lines:
        x = re.findall(r'(\d+)-(\d+),(\d+)-(\d+)', line)
        c1 = (int(x[0][0]), int(x[0][1]))
        c2 = (int(x[0][2]), int(x[0][3]))

        s1 = set(range(c1[0], c1[1]+1))
        s2 = set(range(c2[0], c2[1]+1))
        if len(s1.union(s2)) < len(s1) + len(s2):
            nintersect += 1
    return nintersect


# p1("inputs/4.real.txt")
# p2("inputs/4.real.txt")