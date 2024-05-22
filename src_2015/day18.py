import numpy as np

def read_input(input):
    return np.array([[1 if c == '#' else 0 for c in line] for line in input.splitlines()])

def step(grid, part):
    new_grid = np.zeros_like(grid)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if part == 2:
                if row in [0, grid.shape[0]-1] and col in [0, grid.shape[1]-1]:
                    new_grid[row, col] = 1
                    continue
            n = np.sum(grid[max(0, row-1):min(grid.shape[0], row+2), 
                            max(0, col-1):min(grid.shape[1], col+2)])
            n -= grid[row, col]
            if grid[row, col] == 1:
                new_grid[row, col] = 1 if n in [2, 3] else 0
            else:
                new_grid[row, col] = 1 if n == 3 else 0
    return new_grid

def p1(input):
    input = read_input(input)

    grid = input.copy()
    for _ in range(100):
        grid = step(grid, part=1)
    return np.sum(grid)

def p2(input):
    input = read_input(input)

    grid = input.copy()
    grid[0, 0] = 1
    grid[0, -1] = 1
    grid[-1, 0] = 1
    grid[-1, -1] = 1
    for _ in range(100):
        grid = step(grid, part=2)
    return np.sum(grid)