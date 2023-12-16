import utils

def transpose(input):
    ans = []
    for col in range(len(input[0])):
        s = ""
        for r in range(len(input)):
            s += input[r][col]
        ans.append(s)

    return ans
        
def expand_row(input):
    rows = []
    for row in range(len(input)):
        if "#" not in input[row]:
            rows.append(row)
    return rows

def expand_galaxies(input):
    rows_expanded = expand_row(input)
    transposed = transpose(input)
    cols_expanded = expand_row(transposed)
    return rows_expanded, cols_expanded

def get_galaxy_locs(input):
    locs = []
    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col] == '#':
                locs.append((row, col))
    return locs

def get_dist(start, goal, expand_rows, expand_cols, d=2):
    r_s, c_s = start
    r_g, c_g = goal
    maxrow, minrow = max(r_s,r_g), min(r_s,r_g)
    maxcol, mincol = max(c_s,c_g), min(c_s,c_g)

    base_dist = abs(r_s - r_g) + abs(c_s - c_g)

    rows_covered = set(list(range(minrow, maxrow+1)))
    cols_covered = set(list(range(mincol, maxcol+1)))

    emptys = len(rows_covered.intersection(expand_rows)) + \
                len(cols_covered.intersection(expand_cols))


    return base_dist + ((d-1)*emptys)

total_sum_p2 = 0
def p1(input):
    input = utils.split_and_strip(input)
    rows, cols = expand_galaxies(input)

    locs = get_galaxy_locs(input)

    total_sum = 0
    global total_sum_p2
    for i in range(len(locs)):
        for j in range(i+1, len(locs)):
            dist = get_dist(locs[i], locs[j], rows, cols)
            total_sum += dist
            total_sum_p2 += get_dist(locs[i], locs[j], rows, cols, d=1e6)
    return total_sum


def p2(input):
    return total_sum_p2