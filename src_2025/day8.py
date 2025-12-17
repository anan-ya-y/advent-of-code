import utils
import numpy as np

def dist(a, b):
    return np.linalg.norm(a-b, ord=2)

# arr = [(dist, i, j)]
# val = dist going in
# coords = (i, j) going in
# insert by dist. keep 1k shortest dists. 
def log2insert(arr, val, coords):
    if len(arr) == 0:
        return [(val, *coords)]
    if arr[-1][0] < val:
        arr.append((val, *coords))
        return arr
    if arr[0][0] > val:
        return [(val, *coords)] + arr
    
    low = 0
    high = len(arr) - 1
    while low < high:
        mid = (high + low) // 2
        if arr[mid][0] < val:
            low = mid+1
        else:
            high = mid

    arr = arr[:low] + [(val, *coords)] + arr[low:]
    return arr[:10000] # arbitrarily choosing 4k... I hope that's enough for 1 component


def add_connection(graph, d):
    _, a, b = d
    if a not in graph:
        graph[a] = []
    if b not in graph:
        graph[b] = []


    graph[a].append(b)
    graph[b].append(a)

    return graph

def in_same_component(a, b, components):
    a_comp = None
    b_comp = None
    for i in range(len(components)):
        comp = components[i]
        if a in comp:
            a_comp = i
        if b in comp:
            b_comp = i

    return a_comp == b_comp
    

def main(inp):
    inp = utils.split_and_strip(inp)
    inp = [np.array(list(map(int, line.split(",")))) for line in inp]

    dists = []
    for i in range(len(inp)):
        for j in range(i, len(inp)):
            d = dist(inp[i], inp[j]) if i != j else float('inf')
            # dists = log2insert(dists, d, (i, j))
            dists.append((d, i, j))

    dists.sort(key=lambda x: x[0])

    graph = {} # vertex, [nbrs]
    p1_connections = 10 if len(inp) < 50 else 1000
    for d in dists[:p1_connections]:
        graph = add_connection(graph, d)

    components = utils.connected_components(graph)

    component_sizes = [len(x) for x in components]
    component_sizes.sort(reverse=True)
    p1 = component_sizes[0] * component_sizes[1] * component_sizes[2]
    for pt in range(len(inp)):
        if pt not in graph:
            graph[pt] = []

    for i in range(p1_connections, len(dists)):
        indices = dists[i][1], dists[i][2]

        if in_same_component(indices[0], indices[1], components):
            continue

        graph = add_connection(graph, dists[i])
        components = utils.connected_components(graph)
        if len(components) == 1:
            print(indices, inp[indices[0]], inp[indices[1]])
            p2 = inp[indices[0]][0]* inp[indices[1]][0]
            break

    return p1, p2