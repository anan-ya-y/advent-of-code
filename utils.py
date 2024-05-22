import math
from queue import PriorityQueue
from functools import reduce

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    return [l.strip() for l in lines]


def split_lines(filecontents):
    return filecontents.split("\n")

def split_and_strip(filecontents, character="\n"):
    lines = [l.strip() for l in filecontents.split(character)]
    if lines[-1] == "":
        lines.pop()
    return lines

### If using bitmasks, I guess. 

# b = the bitmask to turn into a set
# elements = the elements that the bitmask represents [values] in order
def bitmask_to_set(b, elements):
    s = set()
    n = len(elements)
    for i in range(n):
        # &ing with 1 gets us the rightmost digit
        if b & 1:
            s.add(elements[i])
        b >>= 1
    return s

# s = the set to turn into a bitmask
# elements = the elements that the bitmask represents [values] in order
def set_to_bitmask(s, elements):
    n = len(elements)
    b = 0
    for i in range(n-1, -1, -1):
        b <<= 1
        b |= (elements[i] in s)
    return b

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

def is_prime(n):
    if n == 1:
        return False
    if n == 2:
        return True
    for i in range(2, math.ceil(math.sqrt(n)+1)):
        if n % i == 0:
            return False
    return True

def prime_factorize(n):
    if n == 1:
        return []
    
    factors = []
    i = 2
    while n > 1:
        if n % i == 0:
            n //= i
            factors.append(i)
        else:
            i += 1

    return factors

def number_of_divisors(n):
    from collections import Counter
    import operator
    prime_factors = prime_factorize(n)
    if prime_factors == []:
        return 1
    pf_counts = Counter(prime_factors).values()
    return reduce(operator.mul, map(lambda x: (x+1), pf_counts))

def sum_of_divisors(n):
    from collections import Counter
    import operator
    prime_factors = prime_factorize(n)
    if prime_factors == []:
        return 1
    pf_vals = Counter(prime_factors).keys()
    pf_counts = Counter(prime_factors).values()
    s = 1
    for val, count in zip(pf_vals, pf_counts):
        s *= (val**(count+1)-1)/(val-1)
    return s

def product_of_divisors(n):
    num_factors = number_of_divisors(n)
    if num_factors % 2 == 0:
        return n ** (num_factors // 2)
    return math.sqrt(n) * (n ** (num_factors // 2))

def get_divisors(n):
    divisors = []
    for i in range(1, math.ceil(math.sqrt(n)+1)):
        if n % i == 0:
            divisors.append(i)
            divisors.append(n // i)
    divisors.sort()
    return divisors

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

def make_graph(vertex_labels, edge_function):
    edge_weights = {}
    neighbors = {}
    edge_weights = {}
    neighbors = {v: [] for v in vertex_labels}
    for u in vertex_labels:
        for v in vertex_labels:
            if edge_function(u, v) is not None:
                edge_weights[(u, v)] = edge_function(u, v)
                neighbors[u].append(v)
    return edge_weights, neighbors

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
    edge_weights, neighbors = make_graph(vertex_labels, edge_function)

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

# RUNS REALLY SLOWLY COMPARED TO BFS IMPLEMENTATION, NOT SURE WHY.
def reachability(start_vertex, neighbors: dict):
    # use bfs
    # q = [start_vertex]
    # visited = set()
    # while len(q) > 0:
    #     u = q.pop(0)
    #     visited.add(u)
    #     for v in neighbors[u]:
    #         if v not in visited:
    #             q.append(v)
    # return visited
    return bfs_with_neighbors(neighbors.keys(), neighbors, start_vertex, None)

# # Returns length of shortest path from start_vertex to target
# # if target is None, returns dict of shortest paths lengths to all vertices.
# # vertex_labels: list of vertices (YOUR labels)
# # edge_function: takes in two vertices and returns the edge weight between them.
# def bfs(vertex_labels, edge_function, start_vertex, target):
#     _, neighbors = make_graph(vertex_labels, edge_function)
#     return bfs_with_neighbors(vertex_labels, neighbors, start_vertex, target)

# Returns length of shortest path from start_vertex to target. 
# if target is None, returns dict of shortest path lengths to all other states. 
# neighbor_generator: function that takes input vertex outputs list of all possible neighbors
def bfs_with_neighbor_generator(neighbor_generator, start_vertex, target=None):
    q = [(start_vertex, 0)]
    dists = {}

    while len(q) > 0:
        u, d = q.pop(0)

        if u in dists:
            continue

        dists[u] = d
        if u == target:
            return dists[u]
        for v in neighbor_generator(u):
            if v not in dists:
                q.append((v, d+1))

    if target is None:
        return dists
    return -1

# Returns length of shortest path from start_vertex to target. 
# if target is None, returns dict of shortest paths lengths to all vertices. 
# vertex_labels: list of vertices (YOUR labels)
# neighbors: dict of vertex: list of neighbors
def bfs_with_neighbors(neighbors:dict, start_vertex, target=None):
    def neighbor_fn(x):
        return neighbors[x]
    return bfs_with_neighbor_generator(neighbor_fn, start_vertex, target)
    # q = [(start_vertex, 0)]
    # dists = {}

    # while len(q) > 0:
    #     u, d = q.pop(0)

    #     if u in dists:
    #         continue

    #     dists[u] = d
    #     if u == target:
    #         return dists[u]
    #     for v in neighbors[u]:
    #         if v not in dists:
    #             q.append((v, d+1))

    # if target is None:
    #     return dists
    # return -1 # no path from start_vertex to target

# def dfs(vertex_labels, edge_function, start_vertex, target):
#     q = [(start_vertex, 0)]
#     visited = set()
#     while len(q) > 0:
#         u, d = q.pop()
#         visited.add(u)
#         if u == target:
#             return d
#         for v in vertex_labels:
#             if v not in visited and edge_function(u, v):
#                 q.append((v, d+1))
#     return -1

# # PROBABLY DOESN'T WORK. 
# def longest_cycle(vertex_labels, edge_function, start_vertex):
#     best_dist = -1
#     for v in vertex_labels:
#         if edge_function(v, start_vertex) is not None:
#             print(v)
#             dist = dfs(vertex_labels, edge_function, start_vertex, v)
#             dist += edge_function(v, start_vertex)
#             best_dist = max(best_dist, dist)

#     return best_dist


def transpose_string_matrix(input):
    ans = []
    for col in range(len(input[0])):
        s = ""
        for r in range(len(input)):
            s += input[r][col]
        ans.append(s)

    return ans