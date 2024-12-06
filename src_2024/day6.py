c = complex
ROTATE = c(0, -1)

import utils

space, startpos = None, None

def parse_input(input):
    global space, startpos
    space = {}
    startpos = None
    input = utils.split_and_strip(input)
    for row in range(len(input)):
        for col in range(len(input[row])):
            space[c(row, col)] = input[row][col]
            if input[row][col] == "^":
                startpos = c(row, col)
                space[c(row, col)] = "."

# returns length of visited & if infinite loop
def simulate(space, startpos, direction):
    visited_positions = set()
    visited_pos_dir = set()
    if startpos not in space:
        return len(visited_positions), False
    pos = startpos
    while True:
        if (pos, direction) in visited_pos_dir:
            return len(visited_positions), True

        visited_positions.add(pos)
        visited_pos_dir.add((pos, direction))
        nextpos = pos + direction
        if nextpos not in space:
            break
        if space[nextpos] == "#":
            direction *= ROTATE
        else:
            pos = nextpos
    return len(visited_positions), False
    
def print_visited():
    global space, visited
    max_rows = max([x.real for x in space])
    max_cols = max([x.imag for x in space])

    for row in range(int(max_rows) + 1):
        for col in range(int(max_cols) + 1):
            pos = c(row, col)
            if pos in visited:
                print("X", end="")
            elif pos in space:
                print(space[pos], end="")
        print()

def main(input):
    parse_input(input)
    
    direction = c(-1, 0)

    p1, _ = simulate(space, startpos, direction)

    npossible = 0
    for pos in space:
        space_duplicate = space.copy()
        if space_duplicate[pos] == "#" or pos == startpos:
            continue
        space_duplicate[pos] = "#"
        _, infinite = simulate(space_duplicate, startpos, direction)
        if infinite:
            npossible += 1
            print(npossible)


    return p1, npossible

