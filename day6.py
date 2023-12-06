import utils
import re
import math

def quadfmla(a, b, c):
    return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a), \
              (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)

def get_match_window(t, d):
    # h = hold time
    # h(t-h) > d
    solns = quadfmla(-1, t, -d)
    solns = [min(solns), max(solns)]
    
    # make sure we are looking at INTEGERS greater than
    if solns[0] == int(solns[0]):
        solns[0] = solns[0] + .01
    if solns[1] == int(solns[1]):
        solns[1] = solns[1] - .01

    # get the window
    earliest = math.ceil(min(solns))
    latest = math.floor(max(solns))
    noptions = latest - earliest + 1

    return noptions

def p1(filename):
    lines = utils.read_file(filename)
    times = re.findall(r'(\d+)+', lines[0])
    distances = re.findall(r'(\d+)+', lines[1])

    times = [int(l) for l in times]
    distances = [int(d) for d in distances]

    product = 1
    for t, d in zip(times, distances):
        noptions = get_match_window(t, d)
        product *= noptions
        print(noptions)

    print(product)

def p2(filename):
    lines = utils.read_file(filename)
    times = re.findall(r'(\d+)+', lines[0])
    distances = re.findall(r'(\d+)+', lines[1])

    t = int(''.join(times))
    d = int(''.join(distances))

    noptions = get_match_window(t, d)
    print(noptions)


p1("inputs/6.real.txt")
p2("inputs/6.real.txt")