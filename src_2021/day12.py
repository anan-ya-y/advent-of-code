import utils

def parse_input(input):
    input = utils.split_and_strip(input)
    graph = {}
    for line in input:
        l = line.split("-")
        if l[0] not in graph:
            graph[l[0]] = []
        graph[l[0]].append(l[1])

        if l[1] not in graph:
            graph[l[1]] = []
        graph[l[1]].append(l[0])
    return graph

def find_paths(map, part):
    def can_visit(cave, path, part):
        if part == 1:
            return cave.isupper() or cave not in path
        # part == 2
        if cave == "start":
            return False
        if cave.isupper():
            return True
        # cave is small
        if cave not in path:
            return True
        # if there's another cave that's twice visited
        small_caves = [c for c in path if c.lower() == c]
        return len(set(small_caves)) == len(small_caves) # True if every small cave visited once
    

    finalized_paths = []

    q = [["start"]]
    while q:
        path = q.pop(0)

        neighbors = map[path[-1]]
        for n in neighbors:
            if not can_visit(n, path, part):
                continue
            if n == "end":
                finalized_paths.append(path + [n])
            else:
                q.append(path + [n])
    return len(finalized_paths)


def p1(input):
    map = parse_input(input)
    return find_paths(map, 1)

def p2(input):
    map = parse_input(input)
    return find_paths(map, 2)