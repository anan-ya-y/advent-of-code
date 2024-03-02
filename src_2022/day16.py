import utils, re
# Thanks hyper-neutrino for the graph compression idea as well as how to do p2! 

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

def compress_graph(graph, flowrates):
    good_valves = [v for v in flowrates if flowrates[v] != 0] + ["AA"]
    distances = {}
    edge_function = lambda u, v: 1 if v in graph[u] else None
    for v1 in good_valves:
        v1dists = utils.bfs(graph.keys(), edge_function, v1, None)
        for v2 in good_valves:
            distances[(v1, v2)] = v1dists[v2]

    return distances, good_valves

mfr_arr = {}
# max flow rate 
# current = human's position
# remaining_time = time left
# opened = valves that are open
def mfr(current, remaining_time, opened, flowrates, distances, bitmask_legend):
    if (current, remaining_time, opened) in mfr_arr:
        return mfr_arr[(current, remaining_time, opened)]
    
    all_valves = set(bitmask_legend)
    opened_set = utils.bitmask_to_set(opened, bitmask_legend)
    unopened_valves = all_valves.difference(opened_set)

    max_flow = 0
    for valve in unopened_valves:
        # check if we can close it
        new_remtime = remaining_time - distances[(current, valve)] - 1
        if new_remtime <= 0:
            continue # we don't have time to open it. 

        new_opened = utils.set_to_bitmask(opened_set.union({valve}), bitmask_legend)
        # new_opened = opened | (1 << bitmask_legend.index(valve))

        flow = flowrates[valve] * new_remtime # we opened this valve. 
        flow += mfr(valve, new_remtime, new_opened, flowrates, distances, bitmask_legend)

        max_flow = max(max_flow, flow)

    mfr_arr[(current, remaining_time, opened)] = max_flow
    return max_flow

def p1(input):
    graph, flowrates = read_input(input)
    distances, good_valves = compress_graph(graph, flowrates)

    x = mfr("AA", 30, 0, flowrates, distances, good_valves)
    return x

def p2(input):
    graph, flowrates = read_input(input)
    distances, good_valves = compress_graph(graph, flowrates)

    best_flow = 0
    max_bitmask = (1 << len(good_valves)) - 1
    for flowval in range(max_bitmask // 2): # //2 beause we'll do the same work twice anyway
        elephant_todos = flowval
        human_todos = max_bitmask - flowval

        elephant_flow = mfr("AA", 26, human_todos, flowrates, distances, good_valves)
        human_flow = mfr("AA", 26, elephant_todos, flowrates, distances, good_valves)
        best_flow = max(best_flow, elephant_flow + human_flow)

    return best_flow




