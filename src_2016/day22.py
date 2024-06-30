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

SIZE="size"
USED="used"
AVAIL="avail"
USE="use"

def print_grid(grid, simple=True):
    max_x = int(max([k.real for k in grid]))
    max_y = int(max([k.imag for k in grid]))
    print("-----")
    for i in range(max_y+1):
        for j in range(max_x+1):
            node = c(j, i)
            if not simple:
                if node in grid:
                    print(f"{grid[node][USED]}/{grid[node][SIZE]}", end=" ")
                else:
                    print(" ", end="")
            else:
                if grid[node][USED] == 0:
                    print("_", end="")
                elif grid[node][USED] > 100:
                    print("#", end="")
                else:
                    print(".", end="")
        print()
    print("-----")

def parse_input(input):
    input = utils.split_and_strip(input)
    regex_expression = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)"
    grid = {}
    for line in input[2:]:        
        k = re.search(regex_expression, line)
        k = list(map(int, k.groups()))
        grid[c(k[0], k[1])] = {
            SIZE: k[2],
            USED: k[3],
            AVAIL: k[4],
            USE: k[5]
        }
    return grid

def execute_swaps(grid, moves):
    for i in range(len(moves)-1):
        current, next = moves[i], moves[i+1]
        grid[current][USED] += grid[next][USED]
        grid[next][USED] = 0
        grid[current][AVAIL ] = grid[current][SIZE] - grid[current][USED]
        grid[next][AVAIL] = grid[next][SIZE] - grid[next][USED]
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

    # Find the empty node
    empty = [k for k, v in grid.items() if v[USED] == 0][0]
    target = max([k for k in grid if k.imag == 0], key=lambda x: x.real)
    print(f"EMPTYLOC: {empty}, TARGETLOC: {target}")

    # move the empty to right next to the target
    def neighbor_generator(node):
        position, swaps = node
        new_grid = execute_swaps(copy.deepcopy(grid), swaps)
        directions = [c(1, 0), c(-1, 0), c(0, 1), c(0, -1)]
        next_positions = []
        for d in directions:
            new_pos = position + d
            if position in grid and new_pos in grid and \
                new_grid[new_pos][USED] <= new_grid[position][AVAIL] and \
                new_pos != position:
                next_positions.append(new_pos)
        # print(node, next_positions)
        return next_positions
    def priority_up(node):
        return node.imag
    
    bfs_target = target-c(1, 0)
    first_part = utils.bfs_return_path(neighbor_generator, empty, bfs_target, \
                                        priority_fn=priority_up)
    grid = execute_swaps(grid, first_part)
    nsteps += len(first_part)-1
    assert len(first_part)-1 == 33, len(first_part)


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
    nmoves_g = target.real-1# ...G_ -> G_... number of moves
    assert nmoves_g == 35, f"nmoves_g: {nmoves_g}"
    nsteps += 5*nmoves_g

    assert nsteps == 33 + 1 + (5*35)
    return nsteps