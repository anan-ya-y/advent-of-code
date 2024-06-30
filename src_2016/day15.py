import utils, re

def parse_input(input):
    input = utils.split_and_strip(input)
    discs = {} # discnum: npositions, startposition
    for line in input:
        l = re.search(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).", line)
        l = list(map(int, l.groups()))
        discs[l[0]] = l[1:]
    return discs

# returns a negative number 
def position_at_time(disc, time):
    return ((disc[1] + time) % disc[0])

def p1(input):
    discs = parse_input(input)
    time = 0
    while True:
        positions = [position_at_time(discs[i], time + i) for i in discs]
        if all([p == 0 for p in positions]):
            return time
        time += 1

def p2(input):
    discs = parse_input(input)
    discs[max(discs.keys())+1]= [11, 0]
    time = 0
    while True:
        positions = [position_at_time(discs[i], time + i) for i in discs]
        if all([p == 0 for p in positions]):
            return time
        time += 1