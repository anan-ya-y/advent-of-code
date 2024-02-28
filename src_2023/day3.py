# # Was given a tip to try with complex numbers! so trying that. 

import utils

C = complex

neighbors = [C(-1,-1), C(-1,0), C(-1,1), \
             C(0,-1),          C(0,1), \
             C(1,-1),  C(1,0),  C(1,1)]

def getNum(grid, coord):
    # Get the FULL number (tuple startcoord, number) at pos
    if coord not in grid or not grid[coord].isnumeric():
        return None
    
    # find start of number
    while coord in grid and grid[coord].isnumeric():
        coord -= C(0, 1)
    coord += C(0, 1)
    startpos = coord

    # find end of number
    num = 0
    while coord in grid and grid[coord].isnumeric():
        num *= 10
        num += int(grid[coord])
        coord += C(0, 1)

    return startpos, num

def get_surrounding_nums(grid, coord):
    surrounding_nums = set()
    for n in neighbors:
        num = getNum(grid, n+coord)
        surrounding_nums.add(num)
    return surrounding_nums

def parseschematic(input):
    lines = utils.split_and_strip(input)

    input_grid = {} # only the non-empty spots
    symbollocs = [] # positions of symbols
    for i in range(len(lines)):
        for j in range(len(lines[i].strip())):
            if lines[i][j] != '.':
                input_grid[C(i,j)] = lines[i][j]
            if not lines[i][j].isnumeric() and \
                    lines[i][j] != ".":
                symbollocs.append(C(i,j))

    return input_grid, symbollocs
    
def p1(input):
    input_grid, symbollocs = parseschematic(input)
    all_adj_nums = set()
    for symbolloc in symbollocs:
        surr_nums = get_surrounding_nums(input_grid, symbolloc)
        all_adj_nums.update(surr_nums)
    all_adj_nums -= {None}
    
    sum = 0
    for n in list(all_adj_nums):
        sum += n[1]
    
    return sum

def p2(input):
    input_grid, symbollocs = parseschematic(input)
    gear_ratios = []
    for symbolloc in symbollocs:
        if input_grid[symbolloc] != "*":
            continue
        surr_nums = get_surrounding_nums(input_grid, symbolloc)
        surr_nums -= {None}
        if len(surr_nums) < 2:
            continue
        gear_ratio = 1
        for num in surr_nums:
            gear_ratio *= num[1]
        gear_ratios.append(gear_ratio)

    return (sum(gear_ratios))

# p1("inputs/3.real.txt")
# p2("inputs/3.real.txt")