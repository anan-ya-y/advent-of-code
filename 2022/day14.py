import utils
C = complex

def read_input(input):
    input = utils.split_and_strip(input)
    occupied = set()
    for line in input:
        positions = line.split(" -> ")
        positions = [list(map(int, p.split(","))) for p in positions]
        for i in range(len(positions)-1):
            xrange = range(positions[i][0], positions[i+1][0]+1) if \
                positions[i][0] < positions[i+1][0] else \
                range(positions[i+1][0], positions[i][0]+1)
            yrange = range(positions[i][1], positions[i+1][1]+1) if \
                positions[i][1] < positions[i+1][1] else \
                range(positions[i+1][1], positions[i][1]+1)

            for x in xrange:
                for y in yrange:
                    occupied.add(C(x,y))
    return occupied

def print_grid(occupied, snow):
    min_x = min([p.real for p in occupied.union(snow)])
    max_x = max([p.real for p in occupied.union(snow)])
    min_y = min([p.imag for p in occupied.union(snow)])
    max_y = max([p.imag for p in occupied.union(snow)])
    for y in range(int(min_y), int(max_y)+1):
        for x in range(int(min_x), int(max_x)+1):
            if C(x,y) in occupied:
                print("#", end="")
            elif C(x, y) in snow:
                print("o", end="")
            else:
                print(".", end="")
        print()

# returns ending pos of particle at startpos
def simulate(startpos, occupied, floor=None):
    # are we in the abyss?
    if floor is None and startpos.imag > max([p.imag for p in occupied]):
        # fall into abyss
        return -1
    if floor is not None and startpos.imag + 1 == floor:
        return startpos
    
    # fall down one step if possible
    if startpos + C(0,1) not in occupied:
        return simulate(startpos + C(0,1), occupied, floor)
    # diagonal down left
    if startpos + C(-1, 1) not in occupied:
        return simulate(startpos + C(-1,1), occupied, floor)
    # diagonal down right
    if startpos + C(1, 1) not in occupied:
        return simulate(startpos + C(1,1), occupied, floor)
    return startpos

def p1(input):
    occupied = read_input(input)
    
    snow = set()
    abyss = False
    nAbyss = 0
    while not abyss:
        s = simulate(C(500,0), occupied.union(snow))
        if s == -1:
            abyss = True
        else:
            snow.add(s)
            nAbyss += 1
    # print_grid(occupied, snow)
    return nAbyss

def p2(input):
    occupied = read_input(input)
    floor = max([p.imag for p in occupied])+2
    
    snow = set()
    n = 0
    while True:
        s = simulate(C(500,0), occupied.union(snow), floor)
        snow.add(s)
        n += 1
        if s == C(500, 0):
            break
    # print_grid(occupied, snow)
    return n

