import utils

def p1(input):
    input = utils.split_and_strip(input)
    input = [[int(k) for k in i.split(",")] for i in input]
    
    # number of exposed = 6*ncubes - 2*ntouching

    ntouching = 0
    for i in range(len(input)):
        cube1 = input[i]
        for j in range(i+1, len(input)):
            cube2 = input[j]
            touching = (abs(cube1[0] - cube2[0]) + \
                        abs(cube1[1] - cube2[1]) + \
                        abs(cube1[2] - cube2[2])) == 1
            if touching:
                ntouching += 1
    return 6*len(input) - 2*ntouching

def p2(input):
    return 1
            