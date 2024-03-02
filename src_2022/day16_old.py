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

def p2(input):
    graph, flowrates = read_input(input)
    
    # x = mfr_elephant("AA","AA", 1, tuple([]), graph, flowrates)
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

mfr_elephant_arr = {}
def mfr_elephant(current_human, current_elephant, minutenum, \
    opened, graph, flowrates):
    if (current_human, current_elephant, minutenum, opened) \
        in mfr_elephant_arr:
        return mfr_elephant_arr[(current_human, current_elephant, \
            minutenum, opened)]
    if (current_elephant, current_human, minutenum, opened) \
        in mfr_elephant_arr:
        return mfr_elephant_arr[(current_elephant, current_human, \
            minutenum, opened)]
    
    if minutenum > 26:
        return 0

    opened = list(opened)
    all_opened_flow = sum([flowrates[o] for o in opened])
    nonzero_flows = [f for f in flowrates if flowrates[f] != 0]
    if len(set(nonzero_flows).difference(set(opened))) == 0: 
        # Everything that matters is open. 
        return all_opened_flow * (26 - minutenum + 1)
    
    options = []
    
    # both skip, elephant only, human only, both turn. 
    
    # both skip:
    for h_c in graph[current_human]:
        for e_c in graph[current_elephant]:
            both_skip = mfr_elephant(h_c, e_c, minutenum+1, tuple(opened), \
                                     graph, flowrates)
            options.append(both_skip)

    # elephant skips, human opens (if human can open)
    if current_human not in opened and flowrates[current_human] != 0:
        o = opened.copy()
        o.append(current_human)
        o.sort()
        for e_c in graph[current_elephant]:
            esho = mfr_elephant(current_human, e_c, minutenum+1, tuple(o),\
                                graph, flowrates)
            options.append(esho)

    # human skips, elephant opens. 
    if current_elephant not in opened and flowrates[current_elephant] != 0:
        o = opened.copy()
        o.append(current_elephant)
        o.sort()
        for h_c in graph[current_human]:
            eohs = mfr_elephant(h_c, current_elephant, minutenum+1, tuple(o),\
                                graph, flowrates)
            options.append(eohs)
    
    # both open
    if current_elephant not in opened and flowrates[current_elephant] != 0 and \
        current_human not in opened and flowrates[current_human] != 0 and \
        current_human != current_elephant: # can't have both open the same thing. 
        o = opened.copy()
        o.append(current_elephant)
        o.append(current_human)
        o.sort()
        bo = mfr_elephant(current_human, current_elephant, minutenum+1, tuple(o),\
                          graph, flowrates)
        options.append(bo)

    # print(current_human, current_elephant)
    ans = max(options) + all_opened_flow

    mfr_elephant_arr[(current_human, current_elephant, minutenum, tuple(opened))] = ans
    # print(current_human, current_elephant, minutenum, opened, ans)
    return ans

