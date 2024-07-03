import utils, re

def parse_input(input):
    input = utils.split_and_strip(input)
    discs = {} # discnum: npositions, startposition
    for line in input:
        l = re.search(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).", line)
        l = list(map(int, l.groups()))
        discs[l[0]] = l[1:]
    return discs

# NOTE: the disc position possibilities are PAIRWISE COPRIME (they're all prime.)
def find_t_using_crt(discs):
    # note that t = -1 * (startpos + discindex) mod (npositions)
    discs = [(d[1], i, d[0]) for i, d in discs.items()] # order: (start, index, npositions)
    discs.sort(key=lambda x: -1*x[2]) # sort by npositions largest to smallest

    # formulate the problem as 
    # t = -val mod positions
    disc_crt = [(-1 * (d[0] + d[1]), d[2]) for d in discs]
    
    conditions_satisfied = 0
    t = disc_crt[conditions_satisfied]
    while conditions_satisfied != len(discs)-1:
        t += discs[conditions_satisfied][2]
        if t % disc_crt[conditions_satisfied+1][1] == disc_crt[conditions_satisfied+1][0]:
            conditions_satisfied += 1
    return t

# returns a negative number 
def position_at_time(disc, time):
    return ((disc[1] + time) % disc[0])

def p1(input):
    discs = parse_input(input)
    find_t_using_crt(discs)

    return -1
    time = 0
    while True:
        positions = [position_at_time(discs[i], time + i) for i in discs]
        if all([p == 0 for p in positions]):
            return time
        time += 1

def p2(input):
    discs = parse_input(input)
    discs[max(discs.keys())+1]= [11, 0]
    time = 3e6
    while True:
        positions = [position_at_time(discs[i], time + i) for i in discs]
        if all([p == 0 for p in positions]):
            return time
        time += 1