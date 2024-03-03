import re, utils, math

GEODE = 3
OBSIDIAN = 2
CLAY = 1
ORE = 0
INGREDIENTS = [ORE, CLAY, OBSIDIAN, GEODE]
ROBOTS_NEEDED = [[ORE], [ORE], [ORE, CLAY], [ORE, OBSIDIAN]]
    # robots_needed[type] is the list of ingredients needed to make type

geodes = {}
reuse = {}
def p1(input):
    global geodes
    global reuse
    input = utils.split_lines(input)
    lines = [re.findall("\d+", i) for i in input]

    s = 0
    for l in lines:
        l = [int(i) for i in l]
        bpnum = l[0]
        costs = [[l[1], 0, 0, 0], 
                 [l[2], 0, 0, 0], 
                 [l[3], l[4], 0, 0],
                 [l[5], 0, l[6], 0]]

        geodes = {}
        g = get_geodes(costs, [1, 0, 0, 0], [0, 0, 0, 0], 24)
        # print(bpnum, len(geodes.keys()), g)
        s += bpnum * g

        if bpnum <= 3:
            reuse[bpnum] = geodes.copy()

    return s


def p2(input):
    return 1
    global geodes
    input = utils.split_lines(input)
    lines = [re.findall("\d+", i) for i in input]

    m = 1
    for i in range(3):
        l = [int(i) for i in lines[i]]
        bpnum = l[0]
        costs = [l[1], l[2], (l[3], l[4]), (l[5], l[6])]
        
        geodes = reuse[bpnum]
        print(bpnum, len(geodes.keys()))
        g = get_geodes(costs, [1, 0, 0, 0], [0, 0, 0, 0], 24)
        print(bpnum, len(geodes.keys()), g)
        m *= g

    return m

def get_geodes(costs, robots, supply, time_left):
    tuple_index = tuple(robots + supply + [time_left])
    # print(costs, tuple_index)
    # tuple_index = tuple([robots + supply + time_left])
    if tuple_index in geodes:
        # print(tuple_index, "found in geodes")
        return geodes[tuple_index]
    
    # ore, clay, obsidian, geode
    
    if time_left <= 0:
        return supply[-1]
        
    max_spend = [
        max([costs[i][ORE] for i in INGREDIENTS]), 
        max([costs[i][CLAY] for i in INGREDIENTS]),
        max([costs[i][OBSIDIAN] for i in INGREDIENTS]),
        99999
    ] # max amount you can spend of each, per round.
    supplycaps = [(max_spend[i]*time_left) for i in range(4)]
        
    # calculate what to build next

    best_geodes = 0 # best amount of geodes we can get

    # build no more, forever. 
    best_geodes = supply[GEODE] + (time_left * robots[GEODE])

    for robot_type in INGREDIENTS:
        if robots[robot_type] >= max_spend[robot_type]:
            continue # making more per round than we can use

        if not all([robots[i] > 0 for i in ROBOTS_NEEDED[robot_type]]):
            continue # we don't have enough robots to make this. 

        churn_time = 0
        for i in ROBOTS_NEEDED[robot_type]:
            churn_time = max(churn_time, 
                             math.ceil((costs[robot_type][i] - supply[i]) / robots[i]))
        
        if churn_time + 1 > time_left:  
            continue

        # churn for churn_time
        # new_supply = [supply[i] + robots[i] *(churn_time+1) 
        #                 for i in INGREDIENTS]

        # build the robot
        new_robots = [robots[i] + (1 if i == robot_type else 0) 
                        for i in INGREDIENTS]
        # new_supply = [min(new_supply[i] - costs[robot_type][i], 
        #                     supplycaps[i]) 
        #                 for i in INGREDIENTS]

        new_supply = [min(supplycaps[i], 
                        supply[i] + robots[i] * (churn_time+1) - costs[robot_type][i]) 
                        for i in INGREDIENTS]

        x = get_geodes(costs, new_robots, new_supply, time_left - churn_time - 1)
        best_geodes = max(best_geodes, x)

    geodes[tuple_index] = best_geodes
    # print(tuple_index, best_geodes)
    return best_geodes

    
