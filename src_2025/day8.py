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
        if len(arr) < 1000:
            arr.append((val, *coords))
        return arr
    if arr[0][0] > val:
        return [(val, *coords)] + (arr[:-1] if len(arr) >= 1000 else arr)
    
    low = 0
    high = len(arr) - 1
    while low < high:
        mid = (high + low) // 2
        if arr[mid][0] < val:
            low = mid+1
        else:
            high = mid

    arr = arr[:low] + [(val, *coords)] + arr[low:]
    return arr[:1000]


    
    

def p1(inp):
    inp = utils.split_and_strip(inp)
    inp = [np.array(list(map(int, line.split(",")))) for line in inp]

    dists = []
    for i in range(len(inp)):
        for j in range(i, len(inp)):
            d = dist(inp[i], inp[j]) if i != j else float('inf')
            dists = log2insert(dists, d, (i, j))

    graph = {} # vertex, [nbrs]
    for d in (dists[:10] if len(inp) < 50 else dists):
        _, a, b = d
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []


        graph[a].append(b)
        graph[b].append(a)

    all_vertices = set(graph.keys())
    components = []
    while len(all_vertices) > 0:
        start = list(all_vertices)[0]
        reachable = utils.reachability(start, graph)
        components.append(reachable)
        all_vertices = all_vertices.difference(reachable)

    component_sizes = [len(x) for x in components]
    component_sizes.sort(reverse=True)
    return component_sizes[0] * component_sizes[1] * component_sizes[2]

