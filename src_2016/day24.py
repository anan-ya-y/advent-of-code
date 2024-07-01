import utils
c = complex
from itertools import permutations

directions = [c(0, 1), c(1, 0), c(0, -1), c(-1, 0)]

def parse_input(input):
    grid = {}
    other_locs = set()
    startpoint = None
    input = utils.split_and_strip(input)
    for y in range(len(input)):
        for x in range(len(input[y])):
            chr = input[y][x]
            if chr != "#":
                grid[c(x, y)] = chr
            if chr.isdigit():
                if chr == "0":
                    startpoint = c(x, y)
                else:
                    other_locs.add(c(x, y))
    return grid, other_locs, startpoint

def get_apsp(grid, all_locs):
    def neighbors(node):
        loc, _ = node
        for d in directions:
            new_loc = loc + d
            if new_loc in grid:
                yield new_loc

    # do pretty much APSP. 
    dists = {}
    for startpos in all_locs:
        for endpos in all_locs:
            if (startpos, endpos) in dists:
                continue
            if startpos == endpos:
                dists[(startpos, endpos)] = 0
                continue
            dist = utils.bfs_with_neighbor_generator(neighbors, startpos, endpos)
            dists[(startpos, endpos)] = dist
            dists[(endpos, startpos)] = dist

    return dists

ans_p1 = -1
ans_p2 = -1
def main(input):
    global ans_p1, ans_p2
    grid, destinations, start = parse_input(input)
    all_locs = destinations.union({start})
    dists = get_apsp(grid, all_locs)
    
    best_dist = 99999999
    best_dist_return = 99999999
    for perm in permutations(all_locs):
        if perm[0] != start:
            continue
        dist = 0
        for i in range(len(perm)-1):
            dist += dists[(perm[i], perm[i+1])]
        best_dist = min(best_dist, dist)

        dist += dists[(perm[-1], start)]
        best_dist_return = min(best_dist_return, dist)

    ans_p1 = best_dist
    ans_p2 = best_dist_return

def p1(input):
    global ans_p1
    main(input)
    return ans_p1

def p2(input):
    global ans_p2
    return ans_p2