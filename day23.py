import utils
C = complex

NORTH = C(-1, 0)
SOUTH = C(1, 0)
EAST = C(0, 1)
WEST = C(0, -1)

directions = {
    ">": EAST, 
    "<": WEST, 
    "^": NORTH,     
    "v": SOUTH
}

def print_hike(map, visited):
    nrows = max([m.real for m in map.keys()])+1
    ncols = max([m.imag for m in map.keys()])+1
    for r in range(int(nrows)):
        for c in range(int(ncols)):
            if C(r, c) in visited:
                print("O", end="")
            else:
                pass
                print(map[C(r, c)], end="")

        print("\t", end="")
        for c in range(int(ncols)):
            print(map[C(r, c)], end="")

        print()

def get_map(input):
    map = {}
    start = -1
    end = -1
    for r in range(len(input)):
        for c in range(len(input[r])):
            map[C(r, c)] = input[r][c]
            if r == 0 and input[r][c] == ".":
                start = C(r, c)
            if r == len(input)-1 and input[r][c] == ".":
                end = C(r, c)
    return map, start, end

def get_longest_path(start, end, neighbors, edge_weights):
    best_path = 0
    stack = [(start, set([start]), 0)]
    while len(stack) > 0:
        v, visited, length = stack.pop(-1)
        available_children = set(neighbors[v]).difference(visited)

        if len(available_children) == 0:
            if end not in visited:
                continue # throw out this path. 
            # print("Finished a path! length {}".format(len(visited)))
            # print_hike(map, visited)
            best_path = max(best_path, length)

        for c in available_children:
            if c in visited:
                continue
            stack.append((c, \
                          visited.union(set([c])), \
                          length+edge_weights[(v, c)]))

    return best_path

def make_edges_longer(neighbors, edge_weights):
    vertices = list(neighbors.keys()).copy()
    for v in vertices:
        if len(neighbors[v]) != 2:
            # print("Vertex {} has {} neighbors".format(v, len(neighbors[v])))
            continue # this vertex is more complicated than we thought. 
        n1, n2 = neighbors[v]
        # print("contracting ", n1, v, n2)
        if (n1, v) in edge_weights and (v, n2) in edge_weights:
            neighbors[n1].remove(v)
            neighbors[n2].remove(v)
            if n2 not in neighbors[n1]:
                neighbors[n1].append(n2)
            if n1 not in neighbors[n2]:
                neighbors[n2].append(n1)
            del neighbors[v]

            if (n1, n2) not in edge_weights:
                edge_weights[(n1, n2)] = -1
            edge_weights[(n1, n2)] = max(edge_weights[(n1, n2)],\
                    edge_weights[(n1, v)] + edge_weights[(v, n2)])
            if (n2, n1) not in edge_weights:
                edge_weights[(n2, n1)] = -1
            edge_weights[(n2, n1)] = max(edge_weights[(n2, n1)],\
                    edge_weights[(n2, v)] + edge_weights[(v, n1)])
            del edge_weights[(n1, v)]
            del edge_weights[(v, n2)]
            del edge_weights[(n2, v)]
            del edge_weights[(v, n1)]
        # print(edge_weights)

    # for n in neighbors:
    #     print(n, neighbors[n])
    # for k in edge_weights:
    #     print(k, edge_weights[k])
    return edge_weights, neighbors
        
def visualize(neighbors):
    import graphviz
    dot = graphviz.Digraph()
    vertices = neighbors.keys()
    for v in vertices:
        dot.node(str(v))
    
    for v in vertices:
        for n in neighbors[v]:
            dot.edge(str(v), str(n))

    dot.render("day23.gv", view=True)

def make_graph(map, edge_function):
    nrows = max([m.real for m in map.keys()])+1
    ncols = max([m.imag for m in map.keys()])+1

    neighbors = {}
    edge_weights = {}
    for r in range(int(nrows)):
        for c in range(int(ncols)):
            v = C(r, c)
            if map[v] == "#":
                continue
            neighbors[v] = []
            for d in [NORTH, SOUTH, EAST, WEST]:
                if v+d in map and edge_function(v, v+d):
                    neighbors[v].append(v+d)
                    edge_weights[(v, v+d)] = 1
    return edge_weights, neighbors

def p1(input):
    input = utils.split_and_strip(input)
    map, start, end = get_map(input)    

    def edge_function(r, c):
        validchars = ".<>^vS"
        if abs(r-c) == 0 or abs(r-c) > 1.1:
            return None
        if map[r] not in validchars or \
            map[c] not in validchars:
            return None
        if map[r] in ".S":
            return 1
        # print(r, c, map[r], map[c])
        if r + directions[map[r]] == c:
            return 1
        
        return None

    edge_weights, neighbors = make_graph(map, edge_function)
    return get_longest_path(start, end, neighbors, edge_weights)

def p2(input):
    input = utils.split_and_strip(input)
    map, start, end = get_map(input)   

    def edge_function(r, c):
        validchars = ".<>^vS"
        if abs(r-c) == 0 or abs(r-c) > 1.1:
            return None
        if map[r] not in validchars or \
            map[c] not in validchars:
            return None
        return 1    
    
    edge_weights, neighbors = make_graph(map, edge_function)
    edge_weights, neighbors = make_edges_longer(neighbors, edge_weights)
    # visualize(neighbors)
    # print(edge_weights, neighbors)
    return get_longest_path(start, end, neighbors, edge_weights)