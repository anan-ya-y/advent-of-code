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
        joltage = tuple(joltage)
        
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
    switch_combos = []
    possible_combos = list(range(1, 2**len(switches)))
    for c in possible_combos:
        state = flip_many_switches(c, switches)
        if state == lights:
            switch_combos.append(c)

    return switch_combos

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

def sub_switch_from_joltage(state, switch):
    return tuple([state[i] - (1 if i in switch else 0) for i in range(len(state))])

def get_odds(joltage):
    x = ""
    for j in joltage:
        x += ("#" if j % 2 == 1 else ".")
    return lights_to_bits(x)

# using the notation from the reddit post
f_history = {} # (joltage, answer)
def f(lights, switches, joltage, nlights, original_switches):
    global f_history
    if joltage in f_history:
        return f_history[joltage]
    
    if all(j == 0 for j in joltage):
        return 0
    
    if any(j < 0 for j in joltage):
        return float('inf')

    light_target = get_odds(joltage)
    scores = []
    base_flips = brute_force(light_target, switches, joltage, nlights)
    for b in base_flips:
        remaining_joltage = joltage
        for i in range(len(switches)):
            if (b >> i) & 1:
                remaining_joltage = sub_switch_from_joltage(remaining_joltage, original_switches[i])

        recurse_joltage = tuple([j//2 for j in remaining_joltage])

        score = count_on_switches(b) + (2*f(lights, switches, recurse_joltage, nlights, original_switches))
        scores.append(score)
    
    if light_target == 0 and not all(j == 0 for j in joltage):
        recurse_joltage = tuple([j//2 for j in joltage])
        score = 2*f(lights, switches, recurse_joltage, nlights, original_switches)
        scores.append(score)

    ans = min(scores) if len(scores) > 0 else float('inf')
    f_history[joltage] = ans
    return ans

###


def p1(inp):
    inp = utils.split_and_strip(inp)
    inp = get_input(inp)

    p1 = 0
    for i in inp:
        lights, switches, joltage, nlights, _ = i
        result = brute_force(lights, switches, joltage, nlights)
        # result = bfs_method(lights, switches, joltage, nlights)
        result = min([count_on_switches(x) for x in result])
        
        p1 += result

    return p1

def p2(inp):
    global f_history
    # https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
    inp = utils.split_and_strip(inp)
    inp = get_input(inp)

    p2 = 0
    for i in inp:
        lights, switches, joltage, nlights, original_switches = i

        f_history = {}
        nsteps =  f(lights, switches, joltage, nlights, original_switches)
        p2 += nsteps

    return p2


