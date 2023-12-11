import utils

C = complex

directions = {
    'N': C(-1, 0), 
    'E': C(0, 1),
    'S': C(1, 0),
    'W': C(0, -1)
}

symbols = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW', 
    'F': 'SE',
}

def find_cycle(edge_function, start_vertex):
    c = start_vertex
    length = 0
    visited = set()
    visited.add(start_vertex)
    while True:
        neighbor_coords = [c+d for d in directions.values()]
        neighbors = [d for d in neighbor_coords if edge_function(c, d)]
        # one neighbor should be in visited already. The next one is ours. 
        # if both are visited, we're done. 
        if neighbors[0] in visited and neighbors[1] in visited:
            return visited
        for n in neighbors:
            if n not in visited:
                c = n
                visited.add(n)
                length += 1
                break

    return -1
        

def process_input(input):
    grid_tiles = {}
    start = None
    free_tiles = []
    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col] == '.':
                free_tiles.append(C(row, col))
            if input[row][col] in symbols:
                grid_tiles[C(row, col)] = \
                    [C(row, col)+directions[d] for d in symbols[input[row][col]]]
            if input[row][col] == 'S':
                start = C(row, col)
    # Add S's neighbors. 
    for d in directions:
        neighbor = start + directions[d]
        if neighbor in grid_tiles and start in grid_tiles[neighbor]:
            grid_tiles[start] = [neighbor]

    return grid_tiles, start, free_tiles

def p1(input):
    input = utils.split_and_strip(input)
    grid_tiles, start, _ = process_input(input)
    
    def edge_fn(u, v):
        if u in grid_tiles and v in grid_tiles[u]:
            return 1
        return None
    
    s = find_cycle(edge_fn, start)

    return int(len(s)/2)
            
def p2(input):
    input = utils.split_and_strip(input)
    grid_tiles, start, free_tiles = process_input(input)

    def edge_fn(u, v):
        if u in grid_tiles and v in grid_tiles[u]:
            return 1
        return None
    
    s = find_cycle(edge_fn, start)

    nInside = 0
    for t in free_tiles:
        r, c = t.real, t.imag
        r = int(r)
        c = int(c)
        
        up = set([t-C(k, 0) for k in range(r+1)])
        down = set([t+C(k, 0) for k in range(1, len(input)-r)])
        left = set([t-C(0, k) for k in range(c+1)])
        right = set([t+C(0, k) for k in range(1, len(input[r])-c)])

        if len(s.intersection(up)) % 2 == 1 and \
            len(s.intersection(down)) % 2 == 1 and \
            len(s.intersection(left)) % 2 == 1 and \
            len(s.intersection(right)) % 2 == 1:
            nInside += 1
            print(t)

    return nInside


