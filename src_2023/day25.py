import utils
import copy
import random
import networkx as nx

def get_product(vertices, neighbors, edges_to_remove):
    new_neighbors = copy.deepcopy(neighbors)
    s1, t1 = edges_to_remove[0]
    for e in edges_to_remove:
        # print(e)
        new_neighbors[e[0]].remove(e[1])
        new_neighbors[e[1]].remove(e[0])

    # 2 reachable components?
    reachable1 = utils.reachability(s1, new_neighbors)
    if len(reachable1) == len(vertices):
        return -1 # dont bother with r2
    reachable2 = utils.reachability(t1, new_neighbors)
    print(edges_to_remove, len(reachable1), len(reachable2))
    if len(reachable1.intersection(reachable2)) == 0 \
        and len(reachable1) + len(reachable2) == len(vertices):
        return len(reachable1) * len(reachable2)
    return -1

def visualize(vertices, edges):
    import graphviz
    dot = graphviz.Digraph()
    dot.nodesep = 10
    for v in vertices:
        dot.node(v)
    for e in edges:
        if e[1] not in vertices or e[1] not in vertices:
            continue
        dot.edge(e[0], e[1])
        
    dot.render("day22.gv", view=True)

def p1(inp):
    inp = utils.split_and_strip(inp)
    G = nx.Graph()
    neighbors = {}
    edges = []
    vertices = set()
    for line in inp:
        line = line.split(":")
        label, nexts = line[0], line[1].strip().split(" ")
        if label not in neighbors:
            neighbors[label] = set()
        neighbors[label] = neighbors[label].union(set(nexts))
        vertices.add(label)
        for n in nexts:
            edges.append((label, n))
            # G.add_edge(label, n, capacity=1)
            edges.append((n, label))
            vertices.add(n)

            if n not in neighbors:
                neighbors[n] = set()
            neighbors[n].add(label)

    G.add_edges_from(edges)
    nx.draw(G, with_labels="True")
    import matplotlib.pyplot as plt
    plt.show()
            
    e1 = input("enter next vertex")
    e2 = input("enter next vertex")
    e3 = input("enter next vertex")
    e4 = input("enter next vertex")
    e5 = input("enter next vertex")
    e6 = input("enter next vertex")
    cut = [(e1, e2), (e3, e4), (e5, e6)]
            
    # cut = [("rkh", "sph"), ("mnf", "hrs"), ("kpc", "nnl")]
    return get_product(vertices, neighbors, cut)

def p2(input):
    return
