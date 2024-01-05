import utils, re

# DP day! 

def read_input(input):
    input = utils.split_and_strip(input)
    flowrates = {}
    graph = {}
    for line in input:
        a = re.findall(r"Valve (\D+) has flow rate=(\d+); (tunnels|tunnel) (leads|lead) to (valves|valve) (\D+)", line)[0]
        key = a[0]
        flowrate = a[1]
        children = [c.strip() for c in a[-1].split(",")]
        graph[key] = children
        flowrates[key] = flowrate
    return graph, flowrates


def p1(input):
    graph, flowrates = read_input(input)
    x = mfr("AA", 1, tuple([]), graph, flowrates)
    return x

mfr_arr = {}
def mfr(current, minutenum, opened, graph, flowrates):
    # = max pressure from minute mn to minute 30 
    # given human start position at current. 
    # and visited contains all visited notdes
    # print(current, minutenum, opened)
    if (current, minutenum, opened) in mfr_arr:
        return mfr_arr[(current, minutenum, opened)]
    
    opened = list(opened)
    all_opened_flow = sum([int(flowrates[o]) for o in opened])

    if minutenum > 30:
        return 0

    if len(opened) == len(graph.keys()): # everything is open
        return all_opened_flow
    if len(opened) % 4 == 0:
        pass
        # print(current, minutenum, opened)


    children = graph[current]
    options = []
    for c in children:
        # leave the valve as-is, just move to next valve
        options.append(mfr(c, minutenum + 1, tuple(opened), graph, flowrates))

        # if closed, open the valve
        if current not in opened and flowrates[current] != 0:
            o = opened.copy()
            o.append(current)
            o.sort()
            next = mfr(c, minutenum + 2, tuple(o), graph, flowrates)
            next += all_opened_flow
            options.append(next)

    ans = max(options) + all_opened_flow
    mfr_arr[(current, minutenum, tuple(opened))] = ans
    return ans