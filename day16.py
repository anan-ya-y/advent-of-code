import utils, re

# DP day!
TIME = 30

def read_input(input):
    input = utils.split_and_strip(input)
    flowrates = {}
    graph = {}
    for line in input:
        a = re.findall(r"Valve (\D+) has flow rate=(\d+); (tunnels|tunnel) (leads|lead) to (valves|valve) (\D+)", line)[0]
        key = a[0]
        flowrate = int(a[1])
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
    if (current, minutenum, opened) in mfr_arr:
        return mfr_arr[(current, minutenum, opened)]
    
    opened = list(opened)
    all_opened_flow = sum([flowrates[o] for o in opened])

    if minutenum > TIME:
        return 0

    nonzero_flows = [f for f in flowrates if flowrates[f] != 0]
    if len(set(nonzero_flows).difference(set(opened))) == 0: 
        # Everything that matters is open. 
        return all_opened_flow * (TIME - minutenum + 1)

    children = graph[current]
    options = []
    # move to next valve
    for c in children:
        opt = mfr(c, minutenum + 1, tuple(opened), graph, flowrates)
        options.append(opt)

    # if closed, open the valve
    if current not in opened and flowrates[current] != 0:
        o = opened.copy()
        o.append(current)
        o.sort()
        next = mfr(current, minutenum + 1, tuple(o), graph, flowrates)
        options.append(next)

    ans = max(options) + all_opened_flow
    mfr_arr[(current, minutenum, tuple(opened))] = ans
    return ans