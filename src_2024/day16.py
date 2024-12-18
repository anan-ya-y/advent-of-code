import utils
import random
c = complex

DIRECTIONS = [c(0, 1), c(0, -1), c(1, 0), c(-1, 0)]
EAST = c(0, 1)

def edge_fn(u, v):
    up, ud = u
    vp, vd = v
    if up == "TARGET" or vp == "TARGET":
        return 0
    return 1 if ud == vd else 1001

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
                                                    set)

    dists_from_end, paths_end = utils.dijkstra_with_generators(TARGET_NODE, \
                                                    neighbor_fn, edge_fn, 
                                                    set)

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

    # plot_path(inp_map, p2)
    return p1, len(p2)
