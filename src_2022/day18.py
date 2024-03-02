import utils

def istouching(cube1, cube2):
    return (abs(cube1[0] - cube2[0]) + \
            abs(cube1[1] - cube2[1]) + \
            abs(cube1[2] - cube2[2])) == 1

def count_exposed(input):
    # number of exposed = 6*ncubes - 2*ntouching

    ntouching = 0
    for i in range(len(input)):
        cube1 = input[i]
        for j in range(i+1, len(input)):
            cube2 = input[j]
            if istouching(cube1, cube2):
                ntouching += 1
    return 6*len(input) - 2*ntouching
    

def p1(input):
    input = utils.split_and_strip(input)
    input = [[int(k) for k in i.split(",")] for i in input]
    return count_exposed(input)
    

def p2(input):
    input = utils.split_and_strip(input)
    input = [tuple(int(k) for k in i.split(",")) for i in input]

    min_x = min([i[0] for i in input]) - 1
    max_x = max([i[0] for i in input]) + 1
    min_y = min([i[1] for i in input]) - 1
    max_y = max([i[1] for i in input]) + 1
    min_z = min([i[2] for i in input]) - 1
    max_z = max([i[2] for i in input]) + 1

    # Idea: construct a graph of the empty space, 
    # then search it for holes that can't reach the outside. 

    # full grid
    edges = {}
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z+1):
                neighbors = []
                if x > min_x:
                    neighbors.append((x-1, y, z))
                if x < max_x:
                    neighbors.append((x+1, y, z))
                if y > min_y:
                    neighbors.append((x, y-1, z))
                if y < max_y:
                    neighbors.append((x, y+1, z))
                if z > min_z:
                    neighbors.append((x, y, z-1))
                if z < max_z:
                    neighbors.append((x, y, z+1))

                edges[(x, y, z)] = neighbors

    # remove all edges from the input
    for cube in input:
        neighbors = edges[cube]
        for neighbor in neighbors:
            if cube in edges[neighbor]:
                edges[neighbor].remove(cube)
        del edges[cube]

    # look for holes:
    outside = (min_x, min_y, min_z)
    holes = []
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z+1):
                if (x, y, z) in input:
                    continue # is not a hole

                # if we can't reach the outside, this is a hole
                if utils.bfs_with_neighbors(edges.keys(), edges, (x, y, z), outside) == -1:
                    holes.append((x, y, z))

    # adjust the input to p1
    return count_exposed(input + holes)