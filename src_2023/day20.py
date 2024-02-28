import utils
import re

class Module:
    def __init__(self, type, label, neighbors):
        self.label = label
        self.type = type
        self.out_neighbors = neighbors
        
        if self.type == "%":
            self.state = False
        elif self.type == "&":
            self.state = {}
        else: # bc module
            self.state = None
        self.flag = -1
    
    # high = True, low = False
    def cycle(self, input, input_giver):
        # print(self.label, "receiving", input)
        if self.type == "%" and not input:
            self.state = not self.state
            return self.state # was off, now on, send high; etc. 
        elif self.type == "&":
            self.state[input_giver] = input
            return not all(self.state.values())
        elif self.type == "b":
            return False

        return None
    
    def add_in_neighbor(self, in_label):
        if self.type == "&":
            self.state[in_label] = False

def make_modules(input):
    modules = {}
    for line in input:
        label, neighbors = line[1:].split(' -> ')
        if label == "roadcaster":
            label = "broadcaster"
        neighbors = neighbors.split(', ')
        modules[label] = Module(line[0], label, neighbors)
        for n in neighbors:
            if n not in modules:
                modules[n] = None

    # non-outgoing models still need state!
    for m in modules:
        if modules[m] is None:
            modules[m] = Module("", m, []) # untyped modules
    
    for m in modules:
        for n in modules[m].out_neighbors:
            modules[n].add_in_neighbor(m)
    

    return modules

def run_cycle(modules, bpnum):
    q = [("broadcaster", False, None)]

    high_voltages = 0
    low_voltages = 0
    while len(q) > 0:
        label, voltage, giver = q.pop(0)
        # print(giver, "sent", voltage, "to", label)

        if voltage:
            high_voltages += 1
        else:
            low_voltages += 1

        new_v = modules[label].cycle(voltage, giver)
        if new_v is None:
            continue

        if modules[label].flag == True and new_v:
            modules[label].flag = bpnum

        q += [(n, new_v, label) for n in modules[label].out_neighbors]
    return high_voltages, low_voltages


def p1(input):
    input = utils.split_and_strip(input)
    modules = make_modules(input)

    # probably worth optimizing but this still runs in .04 seconds..
    high, low = 0, 0
    for _ in range(1000):
        h, l = run_cycle(modules, -1)
        high += h
        low += l
    
    return high * low

def visualize(modules):
    import graphviz
    g = graphviz.Digraph()

    for m in modules:
        g.node(m)

    for m in modules:
        for n in modules[m].out_neighbors:
            g.edge(m, n)
    
    g.render("day20.gv", view=True)

def p2(input):
    input = utils.split_and_strip(input)
    modules = make_modules(input)
    # visualize(modules)
    if "rx" not in modules:
        return -1

    # After attempting to draw the input data out and getting a very ugly result
    # it has come to my attention that there are 4 cycles coming out of bc
    # and they each run sort of independently ish 
    # (and all connect to ft. )

    # so, we are running the 4 cycles independently and taking the LCM to get 
    # rx's low. (thanks reddit)

    rx_parent = None
    for m in modules:
        if "rx" in modules[m].out_neighbors:
            rx_parent = m
            break
        
    flagged = []
    for m in modules:
        if rx_parent in modules[m].out_neighbors:
            modules[m].flag = True
            flagged.append(m)

    i = 1
    found = False
    while not found:
        run_cycle(modules, i)
        i += 1
        found = not(True in [modules[m].flag for m in modules])
        
    lcm = 1
    for m in flagged:
        lcm = utils.lcm(lcm, modules[m].flag)

    return lcm
    