import utils
c = complex
DIRECTIONS = [
    c(1, 0),
    c(0, 1),
    c(-1, 0),
    c(0, -1)
]

space = {}

# neighbor_generator: function that takes input (vertex, path to vertex) outputs list of all possible neighbors
def neighbors(p):
    global space
    pos, _ = p
    neighbors = []
    pos_val = int(space[pos])
    for d in DIRECTIONS:
        if d + pos in space and int(space[pos + d]) == pos_val+1:
            neighbors.append(pos + d)
    return neighbors

def main(input):
    global space
    space = utils.get_complex_space(input, "positions")
    space_vals = utils.get_complex_space(input, "values")

    zero_positions = space_vals["0"]
    nine_positions = set(space_vals["9"])

    # part 1
    p1 = 0
    p2 = 0
    for z in zero_positions:
        reachables = utils.bfs_with_neighbor_generator(neighbors, z, None)
        reachables = set(reachables.keys())
        p1 += len(reachables.intersection(nine_positions))
        
        for r in reachables.intersection(nine_positions):
            paths = utils.bfs_distinct_paths(neighbors, z, r)
            p2 += len(paths)

    return p1, p2





