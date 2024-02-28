import utils
C = complex
possible_directions = [ C(-1, 0),  C(0, -1), C(0, 1),C(1, 0)]

def bfs(start, goal, map):
    queue = [start]
    shortest_pathlength = {start:0}

    while len(queue) > 0:
        v = queue.pop(0)
        if v == goal:
            return shortest_pathlength[v]
        for d in possible_directions:
            if v+d in map and \
                v+d not in shortest_pathlength and \
                map[v+d]-map[v] <= 1:
                shortest_pathlength[v+d] = shortest_pathlength[v] + 1
                queue.append(v+d)
    return -1


def p1(input):
    lines = utils.split_and_strip(input)
    startpos = -1
    endpos = -1
    heightmap = {}
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == "S":
                startpos = C(row, col)
                heightmap[startpos] = 0
            elif lines[row][col] == "E":
                endpos = C(row, col)
                heightmap[endpos] = ord('z')+1-96
            else:
                pos = C(row, col)
                height = ord(lines[row][col])-96
                heightmap[pos] = height

    return bfs(startpos, endpos, heightmap)

def p2(input):
    lines = utils.split_and_strip(input)
    startpos = []
    endpos = -1
    heightmap = {}
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] in "Sa":
                startpos.append(C(row, col))
                heightmap[C(row, col)] = 1
            elif lines[row][col] == "E":
                endpos = C(row, col)
                heightmap[endpos] = ord('z')+1-96
            else:
                pos = C(row, col)
                height = ord(lines[row][col])-96
                heightmap[pos] = height

    min_length = 1e10
    for s in startpos:
        l = bfs(s, endpos, heightmap)
        if l < min_length and l > 0:
            min_length = l
    return min_length