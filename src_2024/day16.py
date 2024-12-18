import utils
import random
c = complex

DIRECTIONS = [c(0, 1), c(0, -1), c(1, 0), c(-1, 0)]
EAST = c(0, 1)

def path_cost(path):
    dir = path[1] - path[0]
    nturns = 1 if dir != EAST else 0
    # breakpoint()
    for i in range(len(path)-1):
        new_dir = path[i+1] - path[i]
        if new_dir != dir:
            nturns += 1
            dir = new_dir

    return 1000*nturns + len(path) - 1

def path_cost_dijkstra(path):
    # if len(set([p[0] for p in path])) != len(path):
        # return float('inf')
    ans = 0
    for i in range(len(path)-1):
        ans += edge_fn(path[i], path[i+1])
    return ans

def edge_fn(u, v):
    up, ud = u
    vp, vd = v
    if up == "TARGET" or vp == "TARGET":
        return 0
    return 1 if ud == vd else 1001


# _cached reduces the runtime SIGNIFICANTLY
visited_cached_fwd = set()
visited_cached_bwd = set()
def visited_fn(v, visited, visited_cached):
    if v[0] in visited_cached:
        return True
    visited_cached.add(v[0])
    return False

def plot_path(inp_map, path):
    xrange = max([int(p.real) for p in inp_map])
    yrange = max([int(p.imag) for p in inp_map])

    for x in range(xrange+1):
        for y in range(yrange+1):
            p = c(x, y)
            if p in path:
                print("o", end="")
            else:
                print(inp_map[p], end="")
        print()

# unfortunately today I am writing my own BFS.. 
def bfs(start_vertex, neighbor_fn, target=None):

    q = []
    q.append((start_vertex, [start_vertex]))
    paths = []
    visited = {}

    while len(q) > 0:
        u, path = q.pop(0)

        # if len(path) > 2:
        #     pc = path_cost(path)

        #     if u in visited and pc > visited[u]:
        #         continue
        #     visited[u] = pc
        # else:
        #     visited[u] = 1

        if u == target:
            paths.append(path)
        else:
            for v in neighbor_fn((u, path)):
                q.append((v, path + [v]))

    return paths, visited

def combine_paths(fwd_path, bwd_path):
    bwd_path = [(p[0], -1*p[1]) for p in bwd_path[::-1]]
    return fwd_path[:-1] + bwd_path

def main(inp):
    inp_map = utils.get_complex_space(inp, "positions")
    inp_symbols = utils.get_complex_space(inp, "values")
    start = inp_symbols["S"][0]
    end = inp_symbols["E"][0]

    TARGET_NODE = ("TARGET", c(0, 0))

    
    def neighbor_fn(node):
        u, ud = node

        if u == "TARGET":
            return [(end, d) for d in DIRECTIONS]
            
        nbrs = []
        if u == end:
            nbrs.append(TARGET_NODE)
        for d in DIRECTIONS:
            new_u = u + d
            if new_u in inp_map and inp_map[new_u] != "#":
                nbrs.append((new_u, d))

        return nbrs
    
    dist, paths = utils.dijkstra_with_generators((start, EAST), \
                                                    neighbor_fn, edge_fn, \
                lambda v, visited: visited_fn(v, visited, visited_cached_fwd))

    dists_from_end, paths_end = utils.dijkstra_with_generators(TARGET_NODE, \
                                                    neighbor_fn, edge_fn, 
                lambda v, visited: visited_fn(v, visited, visited_cached_bwd))

    p1 = dist[TARGET_NODE]
    p2 = set()


    for k in dist:
        k_reverse = (k[0], k[1]*-1)
        if k_reverse not in dists_from_end:
            continue

        pc = dist[k] + dists_from_end[k_reverse]
        if pc != p1:
            continue

        pfront = utils.dijkstra_backtrack(k, paths)
        pend = utils.dijkstra_backtrack(k_reverse, paths_end)

        positions = set([p[0] for p in pfront+pend])
        p2 = p2.union(positions)
    
    p2.remove("TARGET")

    plot_path(inp_map, p2)
    return p1, len(p2)


    exit()

    def neighbors_normal(node):
        u, path = node
        nbrs = []
        for d in DIRECTIONS:
            new_u = u + d
            if new_u in inp_map and inp_map[new_u] != "#" and new_u not in path:
                nbrs.append(new_u)
        return nbrs

    allish_paths, visited = bfs(start, neighbors_normal, end)
    path_costs = [path_cost(p) for p in allish_paths]


    p1 = min(path_costs)
    p2 = set()
    for p in allish_paths:
        if path_cost(p) == p1:
            p2 = p2.union(set(p))
    plot_path(inp_map, p2)

    return p1, len(p2)
