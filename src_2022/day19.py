import re, utils

geodes = {}
def p1(input):
    global geodes
    input = utils.split_lines(input)
    lines = [re.findall("\d+", i) for i in input]

    s = 0
    for l in lines:
        l = [int(i) for i in l]
        bpnum = l[0]
        costs = [l[1], l[2], (l[3], l[4]), (l[5], l[6])]

        geodes = {}
        g = get_geodes(costs, [1, 0, 0, 0], [0, 0, 0, 0], 24)
        print(bpnum, len(geodes.keys()), g)
        s += bpnum * g
    return s


def p2(input):
    pass

def get_geodes(costs, robots, supply, time_left):
    tuple_index = tuple(robots + supply + [time_left])
    # tuple_index = tuple([robots + supply + time_left])
    if tuple_index in geodes:
        # print(tuple_index, "found in geodes")
        return geodes[tuple_index]
    
    # ore, clay, obsidian, geode
    
    if time_left <= 0:
        return supply[-1]
    
    # if we have no time to make a geode robot
    # if time_left < costs[3][1] and robots[2] == 0:
    #     return 0
    
    max_spend = [
        max(costs[0], costs[1], costs[2][0], costs[3][0]), 
        costs[2][1], 
        costs[3][1]
    ] # max amount you can spend of each, per round. 
    def cap_supply(supply):
        # return supply
        return [min(supply[i], max_spend[i]*time_left) for i in range(3)] + [supply[-1]]
        
    # robots just build
    just_build = cap_supply(list(map(sum, zip(robots, supply))))

    # do not build anything
    best_geodes = get_geodes(costs, robots, just_build, time_left-1)

    # build a geode robot 
    if supply[0] >= costs[3][0] and supply[2] >= costs[3][1]:
        new_robots = list(map(sum, zip(robots, [0, 0, 0, 1])))
        new_supply = list(map(sum, zip(just_build, [-costs[3][0], 0, -costs[3][1], 0])))
        new_supply = cap_supply(new_supply)
        best_geodes = max(best_geodes, get_geodes(costs, new_robots, new_supply, time_left-1))
    
    # build an obsidian robot
    if supply[0] >= costs[2][0] and supply[1] >= costs[2][1]:
        new_robots = list(map(sum, zip(robots, [0, 0, 1, 0])))
        new_supply = list(map(sum, zip(just_build, [-costs[2][0], -costs[2][1], 0, 0])))
        new_supply = cap_supply(new_supply)
        best_geodes = max(best_geodes, get_geodes(costs, new_robots, new_supply, time_left-1))
    
    # build a clay robot
    if supply[0] >= costs[1] and robots[1] < max_spend[1]:
        new_robots = list(map(sum, zip(robots, [0, 1, 0, 0])))
        new_supply = list(map(sum, zip(just_build, [-costs[1], 0, 0, 0])))
        new_supply = cap_supply(new_supply)
        best_geodes = max(best_geodes, get_geodes(costs, new_robots, new_supply, time_left-1))

    # build an ore robot
    if supply[0] >= costs[0] and robots[0] < max_spend[0]:
        new_robots = list(map(sum, zip(robots, [1, 0, 0, 0])))
        new_supply = list(map(sum, zip(just_build, [-costs[0], 0, 0, 0])))
        new_supply = cap_supply(new_supply)
        best_geodes = max(best_geodes, get_geodes(costs, new_robots, new_supply, time_left-1))
    
    geodes[tuple_index] = best_geodes
    return best_geodes
