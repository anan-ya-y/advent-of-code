import re, utils
from itertools import permutations

ALL_OBJS = []
ALL_ELEMS = []
MAX_FLOOR = 3
MIN_FLOOR = 0

# floor representation: List of sets. 
# floor+elevator representation = tuple(flors, elevatorpos)
def read_input(input):
    input = utils.split_and_strip(input)
    floors = []
    for i in range(3):
        floors.append(set(input[i].split(", ")))
    floors.append(set())
    return floors

def get_all_objects(floors):
    global ALL_OBJS, ALL_ELEMS
    ALL_OBJS = set.union(*floors)
    ALL_ELEMS = list(set([item[0] for item in ALL_OBJS]))
    return ALL_OBJS

def state_to_string(state):
    floors, elevator = state
    floors = [sorted(floor) for floor in floors]
    return f"{str(floors)}-{elevator}"

def serialize(state):
    floors, e = state
    serial = []
    for f in floors:
        m = [item for item in f if item[1] == "M"]
        g = [item for item in f if item[1] == "G"]
        serial.append((len(m), len(g)))
    return tuple([tuple(serial), e])

perms = {}
def get_all_perms(state):
    floorstate, e = state
    all_perms = permutations(ALL_ELEMS)
    all_permstrings = set()
    s = state_to_string(state)
    if s in perms:
        return perms[s]
    for perm in all_perms:
        newstate = []
        for floor in floorstate:
            newfloor = set()
            for item in floor:
                itemindex = ALL_ELEMS.index(item[0])
                newitem = f"{perm[itemindex]}{item[1]}"
                newfloor.add(newitem)
            newstate.append(newfloor)
        all_permstrings.add(state_to_string((newstate, e)))
    perms[s] = all_permstrings
    return all_permstrings

def equivalent_states(s1, s2):
    perms = get_all_perms(s1)
    return state_to_string(s2) in perms

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

def get_next_states(state):
    floors, e = state
    # print( "floors", floors)
    next_states = []
    for new_e in [e+1, e-1]:
        if new_e > MAX_FLOOR or new_e < MIN_FLOOR:
            continue
        for item1 in floors[e]:
            for item2 in list(floors[e]) + ["--"]:
                if item1 == item2:
                    continue

                new_floors = [f.copy() for f in floors]

                new_floors[e].remove(item1)
                new_floors[new_e].add(item1)
                if item2 != "--":
                    new_floors[e].remove(item2)
                    new_floors[new_e].add(item2)

                if state_valid(new_floors):
                    next_states.append((new_floors, new_e))
    return next_states

def get_min_elevator(start_position, target_position):
    seen_states = set() # set of state strings. 
    q = [(start_position, 0)]
    target_states = get_all_perms(target_position)

    while len(q) > 0:
        state, steps = q.pop(0)
        state_str = state_to_string(state)
        s = serialize(state)
        if s in seen_states:
            continue
        seen_states.add(s)

        if state_str in target_states:
            return steps
        for s in get_next_states(state):
            q.append((s, steps+1))

    return -1

def p1(input):
    floors = read_input(input)
    all_stuff = get_all_objects(floors)

    end_floors = [set()] * (MAX_FLOOR) + [all_stuff]
    end_position = (end_floors, MAX_FLOOR)
    start_position = (floors, 0)

    nsteps = get_min_elevator(start_position, end_position)
    return nsteps

def p2(input):
    floors = read_input(input)
    lobby = set(["DG", "DM", "EG", "EM"])
    floors[0] = floors[0].union(lobby)
    all_stuff = get_all_objects(floors)

    end_floors = [set()] * (MAX_FLOOR) + [all_stuff]
    end_position = (end_floors, MAX_FLOOR)
    start_position = (floors, 0)

    nsteps = get_min_elevator(start_position, end_position)
    return nsteps
