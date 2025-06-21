'''
.
.
HM
LG, LM, MG

is the same state as

LM
HG, HM, LG
'''

import utils

# floor representation: List of sets. 
# floor+elevator representation = tuple(flors, elevatorpos)
def read_input(input):
    state = [
        ["PG", "PM"],
        ["OG", "UG", "RG", "LG"],
        ["OM", "UM", "RM", "LM"], 
        []
    ]

    sample_state = [
        ["HM", "LM"], 
        ["HG"], 
        ["LG"], 
        []
    ]
    return state, 0

def state_valid(floors):
    for floor in floors:
        microchips = [item for item in floor if item[1] == "M"]
        generators = [item for item in floor if item[1] == "G"]

        # if there are no generators, then the microchips are safe
        if len(generators) == 0:
            continue
        
        # okay, there's a generator. 
        # make sure all microchips have partner generators
        for microchip in microchips:
            if f"{microchip[0]}G" not in generators:
                return False
    return True

def serialize(state):
    floors, e = state
    s = []
    for f in floors:
        m = [item for item in f if item[1] == "M"]
        g = [item for item in f if item[1] == "G"]
        s.append(len(m))
        s.append(len(g))

    s.append(e)
    return tuple(s)

def is_end_state(state):
    floors, e = state
    all_but_last = []
    for f in floors[:-1]:
        all_but_last.extend(f)
    return len(all_but_last) == 0

def get_next_states(state):
    next_states = []
    floors, e = state

    next_floors = []
    if e > 0:
        next_floors.append(e-1)
    if e < len(floors)-1:
        next_floors.append(e+1)

    for f in next_floors:
        for item1 in floors[e]:
            for item2 in list(floors[e] + ["--"]):
                if item1 == item2:
                    continue
                if item2 != "--" and item2 > item1:
                    continue

                new_floors = [x.copy() for x in floors]

                new_floors[e].remove(item1)
                new_floors[f].append(item1)
                if item2 != '--':
                    new_floors[e].remove(item2)
                    new_floors[f].append(item2)

                if state_valid(new_floors):
                    next_states.append((new_floors, f))

    return next_states

def get_min_elevator(start_position):
    seen_states = set()
    q = [(start_position, 0)]

    while len(q) > 0:
        state, steps = q.pop(0)
        serialized_state = serialize(state)
        if serialized_state in seen_states:
            continue

        seen_states.add(serialized_state)

        if is_end_state(state):
            return steps
        
        for s in get_next_states(state):
            q.append((s, steps+1))

    return -1

    
def p1(input):
    start_state = read_input(input)
    return get_min_elevator(start_state)

def p2(input):
    start_state = read_input(input)
    start_state[0][0] += ["DG", "DM", "EG", "EM"]
    return get_min_elevator(start_state)
    

