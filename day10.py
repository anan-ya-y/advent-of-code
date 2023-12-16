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
    'F': 'ES',
}

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
    grid_tiles[start] = []
    startdirs = ""
    for d in directions:
        neighbor = start + directions[d]
        if neighbor in grid_tiles and start in grid_tiles[neighbor]:
            grid_tiles[start] += [neighbor]
            startdirs += d

    for s in symbols:
        if startdirs == symbols[s] or startdirs[::-1] == symbols[s]:
            startLetter = s

    return grid_tiles, start, startLetter

def find_loop(grid, start):
    loop = set()
    loop.add(start)

    previous = start
    current = grid[start][1]
    while current != start:
        loop.add(current)

        if grid[current][0] == previous:
            next = grid[current][1]
        else:
            next = grid[current][0]

        previous = current
        current = next

    return loop

def p1(input):
    processed = utils.split_and_strip(input)
    grid, start, _ = process_input(processed)

    loop = find_loop(grid, start)
    return len(loop)//2

def p2(input):
    processed = utils.split_and_strip(input)
    grid, start, startLetter = process_input(processed)

    loop = find_loop(grid, start)
    processed[int(start.real)] = \
        processed[int(start.real)].replace("S", startLetter)
    
    # a little bird told me you only need to check for JL|. 
    nInside = 0
    for row in range(len(processed)):
        inside = False
        for col in range(len(processed[row])):
            c = processed[row][col]
            if C(row, col) in loop:
                if c in 'JL|':
                    # print(row, col)
                    inside = not inside
            elif inside:
                nInside += 1

    return nInside


# correct answer 273. 