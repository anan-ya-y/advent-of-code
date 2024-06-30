import utils, re
import copy
c = complex

adjacent = lambda x, y: (abs(x.real - y.real) <= 1 and \
                         abs(x.imag - y.imag) <= 1 and \
                            x != y)
swappable = lambda x, y, grid: x in grid and \
                                y in grid and \
                                grid[x][USED] <= grid[y][AVAIL] and \
                                x != y
valid = lambda x, y, grid: adjacent(x, y) and swappable(x, y, grid)

SIZE=0
USED=1
AVAIL=2
USE=3

def print_grid(grid):
    max_x = int(max([k.real for k in grid]))
    max_y = int(max([k.imag for k in grid]))
    print("-----")
    for i in range(max_y+1):
        for j in range(max_x+1):
            node = c(j, i)
            if node in grid:
                print(f"{grid[node][USED]}/{grid[node][SIZE]}", end=" ")
            else:
                print(" ", end="")
        print()
    print("-----")

def parse_input(input):
    input = utils.split_and_strip(input)
    regex_expression = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)"
    grid = {}
    for line in input[2:]:        
        k = re.search(regex_expression, line)
        k = list(map(int, k.groups()))
        grid[c(k[0], k[1])] = k[2:]
    return grid

def execute_swaps(grid, moves):
    for i in range(len(moves)-1):
        current, next = moves[i], moves[i+1]
        grid[current][USED] += grid[next][USED]
        grid[next][USED] = 0
    return grid

def p1(input):
    grid = parse_input(input)
    viable_pairs  = 0
    for a in grid:
        for b in grid:
            if grid[a][USED] != 0 and swappable(a, b, grid):
                viable_pairs += 1
    return viable_pairs

def p2(input):
    nsteps = 0
    grid = parse_input(input)
    # print("ORIGINAL GRID")
    # print_grid(grid)

    # Find the empty node
    empty = [k for k, v in grid.items() if v[USED] == 0][0]
    target = max([k for k in grid if k.imag == 0], key=lambda x: x.real)
    # print(f"EMPTYLOC: {empty}, TARGETLOC: {target}")

    # move the empty to right next to the target
    def neighbor_generator(node):
        position, swaps = node
        new_grid = execute_swaps(grid.copy(), swaps)
        # print(f"after execution of {swaps}")
        # print_grid(new_grid)
        directions = [c(1, 0), c(-1, 0), c(0, 1), c(0, -1)]
        next_positions = []
        for d in directions:
            new_pos = position + d
            if valid(position, new_pos, new_grid):
                next_positions.append(new_pos)
        # print(node, next_positions)
        return next_positions
    def euclidean_priority(node):
        return abs(node - target)
    
    first_part = utils.bfs_return_path(neighbor_generator, empty, target-c(1, 0), \
                                        priority_fn=euclidean_priority)
    grid = execute_swaps(grid, first_part)
    nsteps += len(first_part)
    # print("AFTER FIRST PART")
    # print(first_part)
    # print_grid(grid)


    def toptworows_swappable(grid): # the data of any node can fit in any node
        max_data = max([grid[v][USED] for v in grid if v.imag <= 1])
        min_capacity = min([grid[v][SIZE] for v in grid if v.imag <= 1])
        return max_data <= min_capacity
    assert toptworows_swappable(grid), "Top two rows not universally swappable"

    nsteps += 1 # swap so grid has .G_ instead of ._G
    execute_swaps(grid, [target-c(1, 0), target])
    # empty should now be in the position of the target
    assert grid[target][USED] == 0, "Empty node not in target position"

    # it takes 5 turns to go from .G_ to G_.
    nmoves_g = target.real# ...G_ -> G_... number of moves
    nsteps += 5*nmoves_g

    return nsteps