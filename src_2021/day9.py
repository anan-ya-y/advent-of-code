import utils
import numpy as np
from functools import reduce
c = complex

ADJACENT = [c(0, 1), c(1, 0), c(0, -1), c(-1, 0)]

def main(input):
    input = utils.split_and_strip(input)
    map = {}
    for i in range(len(input)):
        for j in range(len(input[i])):
            map[c(j, i)] = int(input[i][j])
    nrows, ncols = len(input), len(input[0])

    local_mins = []
    for i in range(nrows):
        for j in range(ncols):
            adjacents = [map[c(j, i) + a] for a in ADJACENT if c(j, i) + a in map]
            if all(map[c(j, i)] < x for x in adjacents):
                local_mins.append(c(j, i))

    # this only works because "and all other locations will always be part of exactly one basin."
    basins = []
    for pt in local_mins:
        b = set([pt])
        q = [pt]
        while q: # we do bfs
            cur = q.pop(0)
            if map[cur] == 9:
                continue
            b.add(cur)
            for a in ADJACENT:
                if cur+a in map and cur+a not in b:
                    q.append(cur + a)
        basins.append(len(b))

    basins.sort()

    return sum([map[x] for x in local_mins]) + len(local_mins), \
        reduce(lambda x, y: x*y, basins[-3:])
