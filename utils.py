import math

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    return [l.strip() for l in lines]


def split_lines(filecontents):
    return filecontents.split("\n")

def split_and_strip(filecontents):
    lines = [l.strip() for l in filecontents.split("\n")]
    if lines[-1] == "":
        lines.pop()
    return lines

### Frequently used algorithms
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


# Binary sorts an array. 
# comparator takes inputs (a, b) and returns True if a > b
# sorts in increasing order. arr[0] is the smallest element. 
def binary_sort(arr, comparator):
    if len(arr) == 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    bs_left = binary_sort(left, comparator)
    bs_right = binary_sort(right, comparator)

    arr = []
    # Merge the two arrays:
    while len(bs_left) > 0 and len(bs_right) > 0:
        if comparator(bs_right[0], bs_left[0]): # right is better than left
            arr.append(bs_left.pop(0))
        else:
            arr.append(bs_right.pop(0))
    while len(bs_left) > 0:
        arr.append(bs_left.pop(0))
    while len(bs_right) > 0:
        arr.append(bs_right.pop(0))

    return arr


# Performs Dijkstra's. 
# vertex_labels: list of vertices (YOUR labels)
# edge_function: takes in two vertices and returns the edge weight between them. 
#                edge_function = None if no edge exists. 
# start_vertex: the vertex to start from
# returns dict of vertex: distance from start_vertex
def dijkstra(vertex_labels: list, edge_function, start_vertex):
    dist = {v: math.inf for v in vertex_labels}
    prev = {v: None for v in vertex_labels}
    q = [v for v in vertex_labels]
    dist[start_vertex] = 0

    while len(q) > 0:
        u = q[0]
        for v in q:
            if dist[v] < dist[u]:
                u = v

        q.remove(u)

        for v in vertex_labels:
            if v not in q or edge_function(u, v) is None:
                continue
            alt = dist[u] + edge_function(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev

def bfs(vertex_labels, edge_function, start_vertex, target):
    q = [(start_vertex, 0)]
    visited = set()
    while len(q) > 0:
        u, d = q.pop(0)
        visited.add(u)
        if u == target:
            return 1+d
        for v in vertex_labels:
            if v not in visited and edge_function(u, v):
                q.append((v, d+1))
    return -1

def dfs(vertex_labels, edge_function, start_vertex, target):
    q = [(start_vertex, 0)]
    visited = set()
    while len(q) > 0:
        u, d = q.pop()
        visited.add(u)
        if u == target:
            return d
        for v in vertex_labels:
            if v not in visited and edge_function(u, v):
                q.append((v, d+1))
    return -1


# PROBABLY DOESN'T WORK. 
def longest_cycle(vertex_labels, edge_function, start_vertex):
    best_dist = -1
    for v in vertex_labels:
        if edge_function(v, start_vertex) is not None:
            print(v)
            dist = dfs(vertex_labels, edge_function, start_vertex, v)
            dist += edge_function(v, start_vertex)
            best_dist = max(best_dist, dist)

    return best_dist

