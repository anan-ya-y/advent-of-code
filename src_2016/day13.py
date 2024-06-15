import utils
def iswall(x, y, favnumber):
    if x < 0 or y < 0:
        return True
    k = x*x + 3*x + 2*x*y + y + y*y
    k += favnumber
    k = (str(bin(k))[2:]).count("1")
    return k % 2 == 1

isvalid = lambda x, y, f: not iswall(x, y, f)
    
def get_neighbors(x, y, f):
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if isvalid(x+dx, y+dy, f):
            neighbors.append((x+dx, y+dy))
    return neighbors

def p1(input):
    favnumber = int(input)

    start = (1, 1)
    end = (31, 39)

    x = utils.bfs_with_neighbor_generator(\
                        lambda x: get_neighbors(x[0], x[1], favnumber), \
                        start, end)
    return x

def p2(input):
    favnumber = int(input)
    start = (1, 1)
    margin = 55

    def neighbors_inf_bfs(x, y, favnumber):
        if x >= margin or y >= margin:
            return []
        return get_neighbors(x, y, favnumber)

    x = utils.bfs_with_neighbor_generator(\
                        lambda x: neighbors_inf_bfs(x[0], x[1], favnumber), \
                        start)
    first = set([a for a in x if x[a] <= 50])
    return len(first)


    # return len(visited)