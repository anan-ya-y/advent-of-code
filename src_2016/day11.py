import utils, copy
from itertools import combinations, permutations

# FLOORS REPRESENTATION IS:
# [set(), set(), set(), set()]

def read_input(input):
    input = utils.split_and_strip(input)
    floors = []
    for i in range(3):
        elements = input[i].split(", ")
        floors.append(set(elements))
    floors.append(set())
    return floors

def get_all_objects(floors):
    objects = []
    for floor in floors:
        for item in floor:
            if item not in objects:
                objects.append(item)
    return objects

def get_all_elements(floors):
    elements = []
    for f in floors:
        for item in f:
            if item[0] not in elements:
                elements.append(item[0])
    return elements

def is_valid_move(state1, state2):
    def is_valid_floor(floor):
        microchips = [item for item in floor if item[1] == "M"]
        generators = [item for item in floor if item[1] == "G"]

        # if there are no generators, then the microchips are safe
        if len(generators) == 0:
            return True
        
        # okay, there's a generator. 
        # make sure all microchips have partner generators
        for microchip in microchips:
            if f"{microchip[0]}G" not in generators:
                return False
        return True

    start_floors, start_e = state1
    end_floors, end_e = state2

    # elevator has only moved one floor
    if abs(start_e - end_e) != 1:
        return False
    
    for floor in end_floors:
        if not is_valid_floor(floor):
            return False
    return True

def get_next_move(state, lobby=False):
    floors, e = state

    next_positions = []
    for direction in [-1, 1]:
        new_floor = e + direction
        if new_floor < 0 or \
            (new_floor > 3 and not lobby) or \
            (new_floor > 4 and lobby):
            continue

        things_to_move = list(floors[e]) + list(combinations(floors[e], 2))
        for thing in things_to_move:
            if type(thing) is tuple:
                thing = [thing[0], thing[1]]
            else:
                thing = [thing]

            # new_floors = copy.deepcopy(floors)
            new_floors = [f.copy() for f in floors]

            for t in thing:
                new_floors[e].remove(t)
                new_floors[new_floor].add(t)

            if is_valid_move((floors, e), (new_floors, new_floor)):
                next_positions.append((new_floors, new_floor))
    
    # print(state)
    # for p in next_positions:
        # print(next_positions)

    return next_positions

def seralize_floors(flr):
    seen_elements = []
    new_repn = []
    for f in flr:
        this_flr = set()
        for item in f:
            if item[0] not in seen_elements:
                seen_elements.append(item[0])
            index = seen_elements.index(item[0])
            this_flr.add(f"{index}{item[1]}")
        new_repn.append(this_flr)
    return new_repn

def get_all_perms(state, elements):
    floor, e = state

    def get_perm(serialized, p):
        new_flr = []
        for i in range(len(serialized)):
            f = serialized[i]
            new_f = set()
            for item in f:
                index = int(item[0])
                new_f.add(f"{p[index]}{item[1]}")
            new_flr.append(new_f)
        return new_flr

    serialized = seralize_floors(floor)
    all_permutations = list(permutations(elements))
    # ap = []
    # for p in all_permutations:
    #     _p = get_perm(serialized, p)
    #     if _p not in ap:
    #         ap.append(_p)
    # return ap
    return [(get_perm(serialized, p), e) for p in all_permutations]

# no need to try to generalize, this is a custom bfs. 
# state = (floors, elevator)
def custom_bfs(start_pos, end_pos, lobby=False):
    visited = []
    q = [(start_pos, 0)]

    elements = get_all_elements(start_pos[0])
    all_target_tuples = get_all_perms(end_pos, elements)

    while len(q) > 0:
        u, d = q.pop(0)

        if u in visited:
            continue

        all_perms = get_all_perms(u, elements)
        visited += all_perms

        if u in all_target_tuples:
            return d
    
        for v in get_next_move(u, lobby):
            if v not in visited:
                q.append((v, d+1))
        
    return -1


def p1(input):
    floors = read_input(input)
    
    all_stuff = get_all_objects(floors)
    target_floors = [set(), set(), set(), set(all_stuff)]
    end_position = (target_floors, 3)
    start_position = (floors, 0)
    x = custom_bfs(start_position, end_position, lobby=False)
    return x

def p2(input):
    return -1