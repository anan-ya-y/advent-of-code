import utils
C = complex

NORTH = C(-1, 0)
SOUTH = C(1, 0)
EAST = C(0, 1)
WEST = C(0, -1)

def read_floor(input):
    input = utils.split_and_strip(input)
    nrows = len(input)
    ncols = len(input[0])
    map = {}
    for i in range(len(input)):
        for j in range(len(input[i])):
            map[C(i, j)] = input[i][j]

    return map, nrows, ncols

def get_beams_touching(pos, dir, map, places_visited):
    if (pos, dir) in places_visited:
        return set()
    
    places_visited.add((pos, dir))
    current = set([pos])
    if pos not in map:
        return set()
    
    if map[pos] == ".":
        next = get_beams_touching(pos+dir, dir, map, places_visited)
        return next.union(current)

    if (map[pos] == "|" and dir in [EAST, WEST]) or \
        (map[pos] == "-" and dir in [NORTH, SOUTH]):
        # split into 2 
        split1 = get_beams_touching(pos+(dir*C(0, -1)), dir*C(0, -1), map, places_visited)
        split2 = get_beams_touching(pos+(dir*C(0,  1)), dir*C(0,  1), map, places_visited)
        return split1.union(split2).union(current)
    
    if (map[pos] == "|" and dir in [NORTH, SOUTH]) or \
        (map[pos] == "-" and dir in [EAST, WEST]):
        next = get_beams_touching(pos+dir, dir, map, places_visited)
        return next.union(current)
    

    # I wrote the first two of the below lines and 
    # github copilot wrote the rest of the function
    if map[pos] == "\\":
        if dir == NORTH:
            next = get_beams_touching(pos+WEST, WEST, map, places_visited)
        elif dir == SOUTH:
            next = get_beams_touching(pos+EAST, EAST, map, places_visited)
        elif dir == EAST:
            next = get_beams_touching(pos+SOUTH, SOUTH, map, places_visited)
        elif dir == WEST:
            next = get_beams_touching(pos+NORTH, NORTH, map, places_visited)
        return next.union(current)
    
    if map[pos] == "/":
        if dir == NORTH:
            next = get_beams_touching(pos+EAST, EAST, map, places_visited)
        elif dir == SOUTH:
            next = get_beams_touching(pos+WEST, WEST, map, places_visited)
        elif dir == EAST:
            next = get_beams_touching(pos+NORTH, NORTH, map, places_visited)
        elif dir == WEST:
            next = get_beams_touching(pos+SOUTH, SOUTH, map, places_visited)
        return next.union(current)
    
    return current

# Github copilot wrote this whole function
def print_map(map, beams_visited):
    minx = min([p.real for p in map])
    maxx = max([p.real for p in map])
    miny = min([p.imag for p in map])
    maxy = max([p.imag for p in map])

    for i in range(int(minx), int(maxx)+1):
        for j in range(int(miny), int(maxy)+1):
            if C(i, j) in beams_visited:
                print("O", end="")
            elif C(i, j) in map:
                print(map[C(i, j)], end="")
            else:
                print(" ", end="")
        print("")

def p1(input):
    map, _, _ = read_floor(input)

    # oops lol
    import sys
    sys.setrecursionlimit(10000)

    visited = get_beams_touching(C(0, 0), EAST, map, set())

    # print_map(map, set())
    # print()
    # print_map(map, visited)

    return  len(visited)

def p2(input):
    map, nrows, ncols = read_floor(input)

    max_energized = 0
    # check north and south walls first
    for i in range(ncols):
        if C(0, i) in map:
            visited = get_beams_touching(C(0, i), SOUTH, map, set())
            max_energized = max(max_energized, len(visited))
        if C(nrows-1, i) in map:
            visited = get_beams_touching(C(nrows-1, i), NORTH, map, set())
            max_energized = max(max_energized, len(visited))

    # check east and west walls
    for i in range(nrows):
        if C(i, 0) in map:
            visited = get_beams_touching(C(i, 0), EAST, map, set())
            max_energized = max(max_energized, len(visited))
        if C(i, ncols-1) in map:
            visited = get_beams_touching(C(i, ncols-1), WEST, map, set())
            max_energized = max(max_energized, len(visited))

    return max_energized
