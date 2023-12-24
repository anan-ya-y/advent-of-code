import utils
import re
import numpy as np

edges = []
disintegratable = []
labels = []

def visualize():
    global labels, edges
    import graphviz
    g = graphviz.Digraph()

    for m in labels:
        g.node(str(m).ljust(4, "-"))

    for m in edges:
        a, b = m
        g.edge(str(a).ljust(4, "-"), str(b).ljust(4, "-"))
    
    g.render("day22.gv", view=True)


def p1(input):
    global edges, disintegratable, labels
    # sort by bottom z val
    input = utils.split_and_strip(input)
    blocks = [(re.findall(r"(\d+)", line)) for line in input]
    blocks = [list(map(int, blocks[i])) + [i] for i in range(len(blocks))]
    blocks.sort(key = lambda x: x[2]) # bottom x val
    labels = [b[-1] for b in blocks]

    nrows = max([max(b[0], b[3]) for b in blocks])+1
    ncols = max([max(b[1], b[4]) for b in blocks])+1
    heights_from_above = np.zeros((nrows, ncols)) # height/label at that point
    labels_from_above = (np.ones((nrows, ncols)) * -1).astype(object)
    heights_from_above = np.array(heights_from_above)

    for b in blocks:
        # print(b)
        x1, y1, z1, x2, y2, z2, label = b

        heights_window = heights_from_above[x1:x2+1, y1:y2+1]

        dependency_positions = np.where(heights_window == np.max(heights_window))
        dependency_labels = labels_from_above[x1:x2+1, y1:y2+1][dependency_positions]
        # print("AAA", dependency_labels)

        tallness = z2-z1
        heights_from_above[x1:x2+1, y1:y2+1] = \
            min(np.max(heights_from_above[x1:x2+1, y1:y2+1])+1, z1) + tallness
        
        sittingOn = set(dependency_labels.flatten())
        if -1 in sittingOn:
            sittingOn.remove(-1)
        labels_from_above[x1:x2+1, y1:y2+1] = label

        for s in sittingOn:
            edges.append((s, label))
    
    disintegratable = set(b[-1] for b in blocks)
    # a node is not disintegratable if it is the ONLY PARENT of another vertex. 
    for l in labels:
        parents = [e[0] for e in edges if e[1] == l]
        if len(set(parents)) == 1:
            disintegratable = disintegratable.difference(parents)
    
    return len(disintegratable)

def p2(input):
    global edges, disintegratable, labels

    dependents = {}
    myedges = edges.copy()
    
    def getDependents(label):
        children = [e[1] for e in myedges if e[0] == label]
        # remove vertex and outgoing edges
        for c in children:
            myedges.remove((label, c))

        # If children have no parents, they fall too. 
        othersfalling = set()
        for c in children:
            parents = [e[0] for e in myedges if e[1] == c]
            if len(parents) > 0:
                continue
            othersfalling.add(c)
            deps = getDependents(c)
            othersfalling = othersfalling.union(deps)
        
        return othersfalling

    nfalls = 0
    labels.sort()
    for l in labels:
        if l in disintegratable:
            continue
        myedges = edges.copy()
        d = len(getDependents(l))
        nfalls += d
        # print(l, d)

    return nfalls


