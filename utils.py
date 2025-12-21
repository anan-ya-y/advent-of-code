import math
from queue import PriorityQueue
from functools import reduce
import re
import hashlib
c = complex

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

def ss(filecontents, character="\n"):
    return split_and_strip(filecontents, character)

def split_by_whitespace(filecontents):
    return re.split(r'\s+', filecontents)

# keys="positions" gets {complex position: value}
# keys="values" gets {value: [positions]}
def get_complex_space(input, keys="positions"):
    if keys not in ["positions", "values"]:
        raise ValueError("keys must be 'positions' or 'values'")
    input = split_and_strip(input)
    space = {}
    for row in range(len(input)):
        for col in range(len(input[row])):
            if keys == "positions":
                space[c(row, col)] = input[row][col]
            elif keys == "values":
                if input[row][col] not in space:
                    space[input[row][col]] = []
                space[input[row][col]].append(c(row, col))

    return space



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


# graph = {vertices: [neighbors]}
def connected_components(graph):
    all_vertices = set(graph.keys())
    components = []
    while len(all_vertices) > 0:
        start = list(all_vertices)[0]
        reachable = reachability(start, graph)
        components.append(reachable)
        all_vertices = all_vertices.difference(reachable)
    return components

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
    # dist = {v: math.inf for v in vertex_labels}
    # prev = {v: None for v in vertex_labels}
    # dist[start_vertex] = 0
    # visited = set()

    # q = PriorityQueue()
    # queue_counter = 0 # exists as tiebreaker in pq
    # q.put((0, queue_counter, start_vertex))
    # queue_counter += 1

    # while not q.empty():
    #     _, _, u = q.get()
    #     if u in visited:
    #         continue
    #     visited.add(u)

    #     for v in neighbors[u]:
    #         if v in visited: # I think we don't need this. 
    #             continue
    #         alt = dist[u] + edge_weights[(u, v)]
    #         if alt < dist[v]:
    #             dist[v] = alt
    #             prev[v] = u
    #             q.put((dist[v], queue_counter, v))
    #             queue_counter += 1

    # return dist, prev

    def neighbor_fn(x):
        return neighbors[x]
    def edge_fn(x):
        return edge_weights[x]
    
    return dijkstra_with_generators(start_vertex, neighbor_fn, edge_fn)


# visited_structure: data structure to store visited vertices. 
# write a __contains__ function to redefine "v in visited" etc. 
# also create a .add function to add stuff to the visited set
def dijkstra_with_generators(start_vertex, neighbor_fn, edge_fn,\
                             visited_structure=set):
    dist = {}
    prev = {}
    dist[start_vertex] = 0
    prev[start_vertex] = None
    visited = visited_structure()

    q = PriorityQueue()
    queue_counter = 0 # exists as tiebreaker in pq
    q.put((0, queue_counter, start_vertex))
    queue_counter += 1

    while not q.empty():
        _, _, u = q.get()
        if u in visited:
            continue
        visited.add(u)

        for v in neighbor_fn(u):
            if v in visited:
                continue

            if v not in dist:
                dist[v] = math.inf
            if v not in prev:
                prev[v] = None

            alt = dist[u] + edge_fn(u, v)

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                q.put((dist[v], queue_counter, v))
                queue_counter += 1
            assert v in prev
            assert v in dist

    return dist, prev

def dijkstra_backtrack(target, prev_dict):
    path = []
    u = target
    while u is not None and u in prev_dict:
        path.append(u)
        u = prev_dict[u]
    return path[::-1]

    
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
    x = bfs_with_neighbors(neighbors, start_vertex, None)
    return set(x.keys())

def reachability_with_neighbor_generator(start_vertex, neighbor_generator):
    x = bfs_with_neighbor_generator(neighbor_generator, start_vertex, None)
    return set(x.keys())

# # Returns length of shortest path from start_vertex to target
# # if target is None, returns dict of shortest paths lengths to all vertices.
# # vertex_labels: list of vertices (YOUR labels)
# # edge_function: takes in two vertices and returns the edge weight between them.
# def bfs(vertex_labels, edge_function, start_vertex, target):
#     _, neighbors = make_graph(vertex_labels, edge_function)
#     return bfs_with_neighbors(vertex_labels, neighbors, start_vertex, target)
# priorityfn does smaller numbers first 
# state_in_list(x, list) returns True if an equivalent state to x is in list. 
# Returns length of shortest path from start_vertex to target. 
# if target is None, returns dict of shortest path lengths to all other states. 
# neighbor_generator: function that takes input (vertex, path to vertex) outputs list of all possible neighbors
def bfs_with_neighbor_generator(neighbor_generator, start_vertex, target=None, \
                                priorityfn=None, state_in_list=None):
    
    k = bfs_return_path(neighbor_generator, start_vertex, target, \
                               state_in_list, priorityfn)
    if target is not None:
        return len(k) - 1
    
    distances = {}
    for v, path in k.items():
        distances[v] = len(path) - 1

    return distances

# Returns length of shortest path from start_vertex to target. 
# if target is None, returns dict of shortest paths lengths to all vertices. 
# vertex_labels: list of vertices (YOUR labels)
# neighbors: dict of vertex: list of neighbors
def bfs_with_neighbors(neighbors:dict, start_vertex, target=None):
    def neighbor_fn(x):
        x, path = x
        return neighbors[x]
    return bfs_with_neighbor_generator(neighbor_fn, start_vertex, target)

# is_target is a function that takes in a vertex and returns True if it's the target.
def bfs_return_path(neighbors_generator, start_vertex, target=None, \
                    state_in_list=None, priority_fn=None):
    if state_in_list is None:
        state_in_list = lambda x, l: x in l
    if priority_fn is None:
        priority_fn = lambda x: 1

    q = PriorityQueue()
    queue_counter = 0 # pq tiebreaker. 
    q.put((priority_fn(start_vertex), queue_counter, start_vertex, [start_vertex]))
    queue_counter += 1 
    visited = set()
    paths = {} # {vertex: path to vertex}

    # while len(q) > 0:
    while not q.empty():
        # u, path = q.pop(0)
        _, _, u, path = q.get()

        if state_in_list(u, visited):
            continue

        visited.add(u)
        paths[u] = path

        if u == target:
            return path
        for v in neighbors_generator((u, path)):
            if not state_in_list(v, visited):
                # q.append((v, path + [v]))
                q.put((priority_fn(v), queue_counter, v, path + [v]))
                queue_counter += 1
    

    if target is not None: # we wanted the distance to a target.. which we didn't find
        return []
    return paths # we wanted all the paths 

# neighbor_generator: function that takes input (vertex, path to vertex) outputs list of all possible neighbors
# THE GRAPH BETTER HAVE NO CYCLES - maybe cycles ok?? 
# dfs=True does DFS, False does BFS
def bfs_distinct_paths(neighbor_generator, start_vertex, target, priority_fn = None, dfs=True):
    if priority_fn is None:
        priority_fn = lambda x: 1

    paths = []

    q = []
    q.append((start_vertex, [start_vertex]))

    while len(q) > 0:
        u, path = q.pop() if dfs else q.pop(0)

        if u == target:
            paths.append(path)
        else:
            for v in neighbor_generator((u, path)):
                if v not in path: # this should break cycles???
                    q.append((v, path + [v]))
    
    return paths

# recursive
# returns # of paths from start_vertex to target
def dfs_npaths(neighbor_generator, start_vertex, target):
    cache = {}

    def calculate(v):
        if v == target:
            return 1
        
        if v in cache:
            return cache[v]

        npaths = 0
        for n in neighbor_generator((v, None)):
            sub_paths = calculate(n)
            npaths += sub_paths
        cache[v] = npaths
        return npaths
    
    return calculate(start_vertex)

# UNTESTED.
def bfs_distinct_shortest_paths(neighbors_generator, start_vertex, target):
    paths = []

    q = []
    q.append((start_vertex, [start_vertex]))

    while len(q) > 0:
        u, path = q.pop(0)

        if u == target:
            if len(paths) == 0: # this is the SP. 
                # Any future paths we find are equal or longer. 
                paths.append(path)
            elif len(path) > len(paths[0]):
                continue
            else:
                paths.append(path)
        else:
            if len(paths) > 0 and len(path) > len(paths[0]):
                continue # already too long. 
            for v in neighbors_generator((u, path)):
                if v not in path:
                    q.append((v, path + [v]))
    return paths



def longest_path_length(neighbors_generator, start_vertex, target, state_in_list):
    if state_in_list is None:
        state_in_list = lambda x, l: x in l

    q = []
    q.append((start_vertex, [start_vertex]))
    longest_path_length = 0

    while len(q) > 0:
        u, path = q.pop(0)

        if u == target:
            longest_path_length = max(longest_path_length, len(path))
        else:
            for v in neighbors_generator((u, path)):
                if not state_in_list(v, path):
                    q.append((v, path + [v]))
    
    return longest_path_length-1

def transpose_string_matrix(input):
    ans = []
    for col in range(len(input[0])):
        s = ""
        for r in range(len(input)):
            s += input[r][col]
        ans.append(s)

    return ans

# returns {item: count}
def get_frequencies(input):
    freqs = {}
    for i in input:
        if i not in freqs:
            freqs[i] = 0
        freqs[i] += 1
    return freqs

# returns n most frequent as [(item, count)]
# RETURNS EVERYTHING IF TIES. 
def get_n_most_frequent(input, n):
    freqs = get_frequencies(input)
    freqs = list(freqs.items())
    freqs.sort(key=lambda x: x[1], reverse=True) # most frequently first
    
    ans = []
    i = 0
    while i < len(freqs) and len(ans) < n:
        freq = freqs[i][1]
        all_in = [x for x in freqs if x[1] == freq]
        ans.extend(all_in)
        i += len(all_in)
    return ans

def get_md5(s):
    return hashlib.md5(s.encode()).hexdigest()
def md5(s):
    return get_md5(s)

def get_all_chars_in_squarebrackets(s):
    return re.findall(r"\[(\w+)\]", s)

# gets the range, inclusive of a, b, and regardless of increasing or dec
def range_inclusive(a, b):
    if a == b:
        return range(a, a+1)
    if a > b:
        return range(a, b-1, -1)
    return range(a, b+1)

# line stuff
# input: 2 points on the line
def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x2 - x1 == 0:
        return float('inf')
    return (y2 - y1) / (x2 - x1)

# input: 2 poitns from line 1, 2 points from line 2
def get_line_intersection(l1p1, l1p2, l2p1, l2p2):
    # if l2p2[1] == 1:
    #     breakpoint()
    # if either line is vertical, brute force it
    if slope(l1p1, l1p2) == float('inf'):
        if slope(l2p1, l2p2) == float('inf'):
            if min(l1p1[0], l1p2[0]) <= l2p1[0] <= max(l1p1[0], l1p2[0]):
                return (l2p1[0], l1p1[1])
            if min(l1p1[0], l1p2[0]) <= l2p1[1] <= max(l1p1[0], l1p2[0]):
                return (l2p1[1], l1p1[1])
        m2 = slope(l2p1, l2p2)
        x = l1p1[0]
        y = m2 * (x - l2p1[0]) + l2p1[1]
        return (x, y)   \
            if pt_on_line((x, y), l1p1, l1p2) and pt_on_line((x, y), l2p1, l2p2) \
            else None
    if slope(l2p1, l2p2) == float('inf'):
        return get_line_intersection(l2p1, l2p2, l1p1, l1p2)

    m1 = slope(l1p1, l1p2)
    m2 = slope(l2p1, l2p2)
    x1, y1 = l1p1
    x2, y2 = l2p1
    x = (m1*x1 - m2*x2 + y2 - y1) / (m1 - m2)
    y = m1 * (x - x1) + y1

    # round (x, y) to 5 digits
    x = round(x, 5)
    y = round(y, 5)

    return (x, y) \
        if pt_on_line((x, y), l1p1, l1p2) and pt_on_line((x, y), l2p1, l2p2) \
        else None

# input: pt = point to check, point1, point2 = points on the line
def pt_on_line(pt, point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    x, y = pt

    if not (min(x1, x2) <= x <= max(x1, x2) and \
            min(y1, y2) <= y <= max(y1, y2)):
        return False

    if x1==x2 or y1==y2:
        return True
    
    m = (y2-y1)/(x2-x1)
    return ( (y - y1) - m * (x - x1) ) <= 1e-5

   

# Shape stuff

# Construct the edges of a polygon given its vertices
def construct_edges(vertices):
    edges = []
    for i in range(len(vertices)):
        next_idx = (i + 1) % len(vertices)
        edge = (vertices[i], vertices[next_idx])
        edges.append(edge)
    return edges


# ray casting, but at a diagonal (so we never have to worry about grid edges :)
# edges_are_inside = True means that if the point is on an edge, it's considered inside.
def point_in_shape(pt, shape_vertices, shape_edges, edges_are_inside=True):
    max_x = max([v[0] for v in shape_vertices])
    min_y = min([v[1] for v in shape_vertices])

    ray_end = (max_x + 1, min_y - 1)
    ray = (pt, ray_end)

    intersection_points = set()
    for edge in shape_edges:
        if pt == edge[0] or pt == edge[1]:
            return edges_are_inside
        intersection_point = get_line_intersection(*ray, *edge)
        if intersection_point is not None:
            intersection_points.add(intersection_point)
        if intersection_point == pt: # edge point. 
            return edges_are_inside

    return (len(intersection_points) % 2) == 1
 

