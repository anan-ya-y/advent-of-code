# I am not going for efficiency on this one. 
C = complex

directions = {
    ">": C(0, 1),
    "<": C(0, -1),
    "v": C(1, 0),
    "^": C(-1, 0), 
    " ": C(0, 0)
}

walls = set() # set of positions of walls
dims = (0, 0) # dimensions of the grid
end_pos = C(0, 0) # end position

def read_input(input):
    global walls, dims, end_pos
    blizzards = set()
    walls = set()
    for r, row in enumerate(input.split("\n")):
        for c, char in enumerate(row):
            if char in directions:
                blizzards.add((C(r, c), directions[char]))
            elif char == "#":
                walls.add(C(r, c))
    dims = int(max([x.real for x in walls]))+1, int(max([x.imag for x in walls]))+1
    end_pos = C(dims[0]-1, dims[1]-2)
    return blizzards

def move_blizzards(blizzards):
    new_blizzards = set()
    for pos, direction in blizzards:
        new_pos = pos + direction
        if new_pos in walls:
            new_pos += (direction*2)
            new_pos = C(new_pos.real % dims[0], new_pos.imag % dims[1])
        new_blizzards.add((new_pos, direction))
    return new_blizzards

def print_grid(blizzards, cp=None):
    print(get_grid_str(blizzards, cp))

def get_grid_str(blizzards, cp=None):
    bz = set([x[0] for x in blizzards])
    grid = ""
    for row in range(dims[0]):
        for col in range(dims[1]):
            if C(row, col) in walls:
                grid += "#"
            else:
                if C(row, col) in bz:
                    grid += "x"
                elif cp is not None and C(row, col) == cp:
                    grid += "E"
                else:
                    grid += "."
        grid += "\n"
    return grid

def find_path(blizzards, start, goal):
    seen = set()
    pos_queue = [(start, blizzards.copy(), 0)]
    while pos_queue:
        # pull from q, move blizzards, check if we are done
        q = pos_queue.pop(0)
        pos, blizzards, length = q
        # print(pos, length)
        if pos == goal:
            return length, blizzards
        if get_grid_str(blizzards, pos) in seen:
            continue
        seen.add(get_grid_str(blizzards, pos))
        
        new_blizzards = move_blizzards(blizzards)
        bz = set([x[0] for x in new_blizzards])
        
        # find possible directions to go, add to stack
        for direction in directions.values():
            new_pos = pos + direction

            if new_pos.real < 0 or new_pos.imag < 0 or \
                new_pos.real >= dims[0] or new_pos.imag >= dims[1]:
                continue
            if new_pos not in walls and new_pos not in bz:
                pos_queue.append((new_pos, new_blizzards.copy(), length+1))

def p1(input):
    blizzards = read_input(input)
    return find_path(blizzards, C(0, 1), end_pos)[0]

def p2(input):
    blizzards = read_input(input)
    start_pos = C(0, 1)
    end_pos = C(dims[0]-1, dims[1]-2)

    # there can definitely be cacheing done but idc
    p1, blizzards = find_path(blizzards, start_pos, end_pos)
    p2, blizzards = find_path(blizzards, end_pos, start_pos)
    p3, blizzards = find_path(blizzards, start_pos, end_pos)

    return p1+p2+p3