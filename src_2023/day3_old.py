import utils
import numpy as np
import re

symbols = ["*", "#", "+", "$", "/", "@", "%"] 

def get_adjacent_entry_indices(row, col, nrows, ncols):
    # all possible adjacent indices
    a = [(row-1, col-1), (row-1, col), (row-1, col+1), 
         (row, col-1), (row, col), (row, col+1),
         (row+1, col-1), (row+1, col), (row+1, col+1)]
    a.remove((row, col))

    # just the ones within bounds
    b = []
    for i in a:
        if i[0] >= 0 and i[0] < nrows and i[1] >= 0 and i[1] < ncols:
            b.append(i)

    return np.array(b).T

def get_above_row(grid, row, col):
    _, ncols = grid.shape
    if row == 0: # no above row
        return np.array(['.']*3)
    if col == 0:
        return ''.join(grid[row-1, col:col+2])
    if col == ncols-1:
        return ''.join(grid[row-1, col-1:col+1])
    return ''.join(grid[row-1, col-1:col+2])
def get_below_row(grid, row, col):
    nrows, ncols = grid.shape
    if row == nrows-1: # no below row
        return np.array(['.']*3)
    if col == 0:
        return ''.join(grid[row+1, col:col+2])
    if col == ncols-1:
        return ''.join(grid[row+1, col-1:col+1])
    return ''.join(grid[row+1, col-1:col+2])

def count_nums(arr):
    return len(re.findall(r'\d+', '.'.join(arr)))
    

def propagate_numbers(row, col, original_grid, valid_grid):
    if valid_grid[row, col].isdigit():
        # copy over just the adjacent symbols
        try:
            valid_grid[row, col+1] = original_grid[row, col+1]
        except:
            pass

        try:
            valid_grid[row, col-1] = original_grid[row, col-1] 
        except:
            pass
    return valid_grid
            
def get_numbers_from_grid(grid):
    strs = [''.join(list(row)) for row in grid]
    wholestr = ';'.join(strs)
    return re.findall(r'\d+', wholestr)

def get_grids(lines):
    ncols, nrows = len(lines[0].strip()), len(lines)

    valid_grid = [['.']*ncols]*nrows
    original_grid = []
    for line in lines:
        original_grid.append(list(line.strip()))
    original_grid = np.array(original_grid)
    valid_grid = np.array(valid_grid)
    return valid_grid, original_grid, nrows, ncols

def fill_remaining_grid(valid_grid, original_grid):
    # get stuff next to numbers. Go forward and backwards. 
    for row in range(len(original_grid)):
        for col in range(len(original_grid[0])):
            valid_grid = propagate_numbers(row, col, original_grid, valid_grid)
    for row in range(len(original_grid))[::-1]:
        for col in range(len(original_grid[0]))[::-1]:
            valid_grid = propagate_numbers(row, col, original_grid, valid_grid)
    return valid_grid

def part1_solution(filename):
    lines = utils.read_file(filename)
    # This is gonna be really weird, but whatever. 
    valid_grid, original_grid, nrows, ncols = get_grids(lines)
    
    # get stuff adjacent to symbols
    for row in range(len(original_grid)):
        for col in range(len(original_grid[0])):
            if not original_grid[row, col].isdigit() \
                and original_grid[row, col]!= '.':
                # copy over just the adjacent symbols
                adj_rows, adj_cols = get_adjacent_entry_indices(row, col, \
                                                                nrows, ncols)
                valid_grid[adj_rows, adj_cols] = original_grid[adj_rows, adj_cols]
    
    valid_grid = fill_remaining_grid(valid_grid, original_grid)
    nums = get_numbers_from_grid(valid_grid)
    print(sum(map(int, nums)))

def part2_solution(filename):
    lines = utils.read_file(filename)
    valid_grid, original_grid, nrows, ncols = get_grids(lines)

    for row in range(nrows):
        for col in range(ncols):
            if original_grid[row, col] == "*":
                above_row = get_above_row(original_grid, row, col)
                below_row = get_below_row(original_grid, row, col)
                print(above_row, below_row)
                sides = []
                if col > 0: 
                    sides.append (original_grid[row, col-1])
                if col < ncols:
                    sides.append(original_grid[row, col+1])
                nnums = count_nums([above_row, below_row] + sides)
                if nnums >=2:
                    # copy over just the adjacent symbols
                    adj_rows, adj_cols = get_adjacent_entry_indices(row, col, \
                                                                    nrows, ncols)
                    valid_grid[adj_rows, adj_cols] = original_grid[adj_rows, adj_cols]


    valid_grid = fill_remaining_grid(valid_grid, original_grid)
    nums = get_numbers_from_grid(valid_grid)
    print(sum(map(int, nums)))

part1_solution("inputs/3.real.txt")
# part2_solution("inputs/3.sample.txt")