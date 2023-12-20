import utils

C = complex

NORTH = C(-1, 0)
SOUTH = C(1, 0)
EAST = C(0, 1)
WEST = C(0, -1)

TURNRIGHT = C(0, -1)
TURNLEFT = C(0, 1)

def make_graph(map, minstepsize=1, maxstepsize=3):
    vertices = []
    neighbors = {}
    edge_weights = {}

    for m in map:
        if m == "target":
            continue
        for d in [NORTH, SOUTH, EAST, WEST]:
            vertices.append((m, d))
    
    for m in map:
        if m == "target":
            continue
        for d in [NORTH, SOUTH, EAST, WEST]:
            neighbors[(m, d)] = []
            valid_dirs = [d * TURNLEFT, d*TURNRIGHT]
            for vd in valid_dirs:
                for i in range(minstepsize, maxstepsize+1):
                    if m + (vd*i) in map:
                        neighbors[(m, d)].append((m + (vd*i), vd))
                        edge_weights[((m, d), (m + (vd*i), vd))] = \
                            sum(map[m + (vd*k)] for k in range(1, i+1))
                    
    # add start and end vertices
    vertices += ["start", "end"]
    neighbors["start"] = [(C(0, 0), d) for d in [NORTH, SOUTH, EAST, WEST]]
    edge_weights[("start", (C(0, 0), d))] = map[C(0, 0)]
    neighbors["end"] = []
    for d in [NORTH, SOUTH, EAST, WEST]:
        neighbors[(map["target"], d)] = ["end"]
        edge_weights[((map["target"], d), "end")] = 0
    
    return vertices, neighbors, edge_weights

def p1(input):
    map = read_map(input)
    
    vertex_labels, neighbors, edge_weights = make_graph(map)
    print("starting Dijkstra")
    dist, prev = utils.dikjstra_with_neighbors(vertex_labels, neighbors, \
                                               edge_weights, "start") 
    return (dist["end"] - map[C(0, 0)])   
    


    # DIJKSTRA ATTEMPT #1: took too long because of in-dijkstra graph const
    # vertices are (x, last_dir) 
    def edge_function(u, v):
        # handle start and end vertices
        if u == "start" and v[0] == C(0, 0):
            return map[C(0, 0)]
        if v == "end" and u[0] == map["target"]:
            return 0
        if u in ["start", "end"] or v in ["start", "end"]:
            return None

        ux, ud = u
        vx, vd = v
        # ux to vx must be less than 3
        # ud and vd must not be the same or backwards to each other
        # vd must be the direction of ux to vx
        # don't need to check if it's in the map;
        # vertices are already generated that way. 

        if ud == vd or ud == -vd:
            return None
    
        if vx == ux+vd:
            return map[vx]
        if vx == ux + (2*vd):
            return map[ux+vd] + map[vx]
        if vx == ux + (3*vd):
            return map[ux+vd] + map[ux+(2*vd)] + map[vx]
        
        return None
    
    def vertex_labels():
        labels = []
        for m in map:
            if m == "target":
                continue
            for d in [NORTH, SOUTH, EAST, WEST]:
                labels.append((m, d))
        labels += ["start", "end"]
        return labels
    # dist, prev = utils.dijkstra(vertex_labels(), \
    #                             edge_function, \
    #                             "start")
    # return (dist["end"] - map[C(0, 0)])




    # DP SOLUTION
    # find the min heat loss from start to target
    # m = fill_mhl(map)
    
    # for x in m:
    #     print(x, m[x])

    # return m[(C(0, 0), EAST, 0, 0)] - map[C(0, 0)]

def p2(input):
    return

def read_map(input):
    input = utils.split_and_strip(input)

    map = {}
    for i in range(len(input)):
        for j in range(len(input[0])):
            map[C(i, j)] = int(input[i][j])
    
    map["target"] = C(len(input)-1, len(input[0])-1)

    return map





### ABANDONED DP SOLUTION (works on the samples, but too slow) ###

def fill_mhl(map):
    memo_arr = {}

    for pathlength in range(len(map))[::-1]:
        print(pathlength)
        for s in range(4)[::-1]:
            for x in map:
                if x == "target":
                    continue
                for d in [NORTH, SOUTH, EAST, WEST]:
                            ans = mhl(x, d, s, pathlength, map, memo_arr)
                            memo_arr[(x, d, s, pathlength)] = ans
                            # print(x, d, s, pathlength, "\t", ans)

    return memo_arr

# MHL(x, d, s): min heat loss from x to bottom right corner 
#         given that we have been moving dir d for s steps
#         (not including position x)
"""
MHL(x, d, s) = options: move forward or change directions
            if x not in map, inf. if x in target, 0. 
            min(
                mhl(go straight, d, s+1) + heat(next position) if s < 3
                mhl(go left, left, 1) + heat(next position)
                mhl(go right, right, 1) + heat(next position)
            )

add Pathlength arg to avoid inf loops
            
Evaluation order: decreasing s, decreasing pathlength, d and x don't matter
"""
def mhl(x, d, s, pathlength, map, memo_arr):
    if (x, d, s, pathlength) in memo_arr:
        return memo_arr[(x, d, s, pathlength)]
    # print("CALCULATING", x, d, s, pathlength, "length of memo_arr", len(memo_arr))
    if x == map["target"]:
        return map[x]
    if x not in map or pathlength > len(map)-1:
        return float("inf")
    
    # go straight
    straight = mhl(x+d, d, s+1, pathlength+1, map, memo_arr) if s < 3 else float("inf")

    # turn left
    left_next_pos = x + (d * TURNLEFT)
    left_next_dir = d*TURNLEFT
    left = mhl(left_next_pos, left_next_dir, 1, pathlength+1, map, memo_arr)

    # turn right
    right_next_pos = x + (d * TURNRIGHT)
    right_next_dir = d*TURNRIGHT
    right = mhl(right_next_pos, right_next_dir, 1, pathlength+1, map, memo_arr)

    ans = map[x] + min(straight, left, right)
    return ans

