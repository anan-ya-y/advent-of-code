# I am not going for efficiency on this one. 
C = complex

directions = {
    ">": C(0, 1),
    "<": C(0, -1),
    "v": C(1, 0),
    "^": C(-1, 0)
}

blizzards = set() # set of tuples (position, direction) of blizzard
walls = set() # set of positions of walls
dims = (0, 0) # dimensions of the grid

def read_input(input):
    global blizzards, walls, dims
    blizzards = set()
    walls = set()
    for r, row in enumerate(input.split("\n")):
        for c, char in enumerate(row):
            if char in directions:
                blizzards.add((C(r, c), directions[char]))
            elif char == "#":
                walls.add(C(r, c))

    dims = int(max([x.real for x in walls]))+1, int(max([x.imag for x in walls]))+1
    print(dims)

def move_blizzards():
    global blizzards
    new_blizzards = set()
    for pos, direction in blizzards:
        new_pos = pos + direction
        if new_pos in walls:
            new_pos += (direction*2)
            new_pos = C(new_pos.real % dims[0], new_pos.imag % dims[1])
        new_blizzards.add((new_pos, direction))
    blizzards = new_blizzards

def print_grid():
    bz = set([x[0] for x in blizzards])
    for row in range(dims[0]):
        for col in range(dims[1]):
            if C(row, col) in walls:
                print("#", end="")
            else:
                if C(row, col) in bz:
                    print("x", end="")
                else:
                    print(".", end="")
        print()


def p1(input):
    read_input(input)

def p2(input):
    return 0