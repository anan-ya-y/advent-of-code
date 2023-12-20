import math
from queue import PriorityQueue

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

def to_base_n(dec_num, n):
    ans = 0
    ndigits = int(math.log(dec_num, n)) + 1
    for i in range(ndigits-1, -1, -1):
        ans *= 10
        ans += (dec_num // (n**i))
        dec_num %= (n**i)

    return ans

def from_base_n(num, n):
    ans = 0
    for i in range(len(str(num))):
        ans += (num % 10) * (n**i)
        num //= 10
    return ans


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


# Performs Dijkstra's. Slowly, because can't find graph neighbors quickly.
# vertex_labels: list of vertices (YOUR labels)
# edge_function: takes in two vertices and returns the edge weight between them. 
#                edge_function = None if no edge exists. 
# start_vertex: the vertex to start from
# returns dict of vertex: distance from start_vertex
def dijkstra(vertex_labels: list, edge_function, start_vertex):
    print("Beginning dijkstra preprocessing O(n^2)")
    print("n=", len(vertex_labels))

    # Make edge_weights dict, so that it's easier to find neighbors
    edge_weights = {}
    neighbors = {v: [] for v in vertex_labels}
    for u in vertex_labels:
        for v in vertex_labels:
            if edge_function(u, v) is not None:
                edge_weights[(u, v)] = edge_function(u, v)
                neighbors[u].append(v)

    print("Dikjstra preprocessing done. Starting actual algorithm.")
    return dikjstra_with_neighbors(vertex_labels, neighbors, \
                                   edge_weights, start_vertex)


def dikjstra_with_neighbors(vertex_labels: list, neighbors:dict, \
                            edge_weights:dict, start_vertex):
    dist = {v: math.inf for v in vertex_labels}
    prev = {v: None for v in vertex_labels}
    dist[start_vertex] = 0
    visited = set()

    q = PriorityQueue()
    queue_counter = 0 # exists as tiebreaker in pq
    q.put((0, queue_counter, start_vertex))
    queue_counter += 1

    while not q.empty():
        _, _, u = q.get()
        if u in visited:
            continue
        visited.add(u)

        for v in neighbors[u]:
            if v in visited: # I think we don't need this. 
                continue
            alt = dist[u] + edge_weights[(u, v)]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                q.put((dist[v], queue_counter, v))
                queue_counter += 1

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


def transpose_string_matrix(input):
    ans = []
    for col in range(len(input[0])):
        s = ""
        for r in range(len(input)):
            s += input[r][col]
        ans.append(s)

    return ans