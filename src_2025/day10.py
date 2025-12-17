import utils, re
def get_input(inp):
    clean_inputs = []
    for i in inp:
        # lights
        lights = re.findall(r'\[(.*?)\]', i)[0]
        nlights = len(lights)
        lights = lights_to_bits(lights)

        # switches
        switches = re.findall(r'\(([^()]*)\)', i)
        switches = [list(map(int, x.split(','))) for x in switches]
        original_switches = switches.copy()
        switches = [switch_to_bits(x, nlights) for x in switches]
    
        # joltage
        joltage = re.findall(r'\{(.*?)\}', i)
        joltage = list(map(int, joltage[0].split(','))) 
        
        clean_inputs.append((lights, switches, joltage, nlights, original_switches))

    return clean_inputs 

def lights_to_bits(l):
    return int(l.replace(".", '0').replace("#", '1'), 2)

def switch_to_bits(s, nlights):
    switch = list('0' * nlights)
    for button in s:
        switch[button] = '1'
    return int(''.join(switch), 2)

#### 

def count_on_switches(switch_mask):
    return bin(switch_mask).count('1')


def flip_single_switch(state, switch):
    return state ^ switch # xor

def flip_many_switches(switch_mask, switches):
    current_state = 0
    for i in range(len(switches)):
        if (switch_mask >> i) & 1:
            current_state = flip_single_switch(current_state, switches[i])

    return current_state


def brute_force(lights, switches, joltage, nlights):
    best_switches = 999
    possible_combos = list(range(1, 2**len(switches)))
    for c in possible_combos:
        state = flip_many_switches(c, switches)
        if state == lights:
            best_switches = min(count_on_switches(c), best_switches)

    return best_switches
        
def bfs_method(lights, switches, joltage, nlights):
    # vertices = switch masks (integer)
    # edges = next possible switch mask
    def neighbor_generator(x):
        v, _ = x
        neighbors = []
        for i in range(len(switches)):
            new_v = v | (1 << i)
            neighbors.append(new_v)

        return neighbors

    # have to rewrite bfs for the flip_many_switches check.... 
    q = [0]
    visited = set()
    while len(q) > 0:
        current = q.pop(0)
        if current in visited:
            continue

        if flip_many_switches(current, switches) == lights:
            return count_on_switches(current)

        visited.add(current)
        neighbors = neighbor_generator((current, None))
        for n in neighbors:
            if n not in visited:
                q.append(n)

    return -1

####

def add_switch_to_joltage(state, switch):
    return tuple([state[i] + (1 if i in switch else 0) for i in range(len(state))])

###


def p1(inp):
    inp = utils.split_and_strip(inp)
    inp = get_input(inp)

    p1 = 0
    for i in inp:
        lights, switches, joltage, nlights, _ = i
        # result = brute_force(lights, switches, joltage, nlights)
        result = bfs_method(lights, switches, joltage, nlights)
        
        p1 += result

    return p1

def p2(inp):
    inp = utils.split_and_strip(inp)
    inp = get_input(inp)

    p2 = 0
    for i in inp:
        lights, switches, joltage, nlights, original_switches = i

        def neighbor_generator(x):
            v, _ = x
            neighbors = []
            print(v, joltage)

            # if we've gone too far, stop
            if any([v[i] > joltage[i] for i in range(len(joltage))]):
                return []
            
            # Add each switch
            for s in original_switches:
                new_v = v
                for i in range(10):
                    new_v = add_switch_to_joltage(new_v, s)
                    neighbors.append(new_v)

            return neighbors
        
        ans = utils.bfs_return_path(neighbor_generator, tuple([0]*len(joltage)), tuple(joltage))
        p2 += len(ans) - 1
        return 1
    return p2


