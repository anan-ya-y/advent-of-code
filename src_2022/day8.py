import numpy as np
import utils

def get_visible_trees(grid):
    visible = np.zeros(grid.shape)
    visible[:, 0] = 1
    visible[:, -1] = 1
    visible[0, :] = 1
    visible[-1, :] = 1

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            val = grid[row, col]
            # top, buttom, left, right
            if np.all(val - grid[:row, col] > 0) or \
                np.all(val - grid[row+1:, col] > 0) or \
                np.all(val - grid[row, :col] > 0) or \
                np.all(val - grid[row, col+1:] > 0): 
                visible[row, col] += 1

    return visible


def p1(input):
    lines = utils.split_and_strip(input)
    grid = np.array([list(line) for line in lines]).astype(int)
    visible = get_visible_trees(grid)
    # print(grid)
    # print(visible)

    return np.sum(visible > 0)
    # There are many ways I could do this, but I'm going to go with brute force


def scenic_score(grid):
    # DP, because 374
    scenic_score = np.zeros(grid.shape)
    gridmax=np.max(grid)
    for row in range(grid.shape[0]):
        last_index_height_atleast={}
        for i in range(gridmax+1):
            last_index_height_atleast[i] = 0
        for col in range(grid.shape[1]):
            val = grid[row, col]
            if col == 0:
                scenic_score[row, col] = 0
            elif val < grid[row, col-1]:
                scenic_score[row, col] = 1
            elif val == grid[row, col-1]:
                scenic_score[row, col] = 0
            elif val > grid[row, col-1]:
                scenic_score[row, col] = col-last_index_height_atleast[val]
            for i in range(1, val+1):
                last_index_height_atleast[i] = col
                
    return scenic_score


def p2(input):
    lines = utils.split_and_strip(input)
    grid = np.array([list(line) for line in lines]).astype(int)

    scenic_scores = np.ones(grid.shape)
    for i in range(4):
        rotated_grid = np.rot90(grid, i)
        rotated_scenic = scenic_score(rotated_grid)
        regular_scenic = np.rot90(rotated_scenic, -i)
        scenic_scores *= regular_scenic

    print(scenic_scores)
    return np.max(scenic_scores)