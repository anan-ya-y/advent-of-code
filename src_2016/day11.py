import utils, copy
from queue import PriorityQueue
from itertools import permutations

def read_input(input):
    input = utils.split_and_strip(input)
    floors = []
    for i in range(3):
        floors.append(input[i].split(", "))
    floors.append([])
    floors = [tuple(sorted(f)) for f in floors]
    return tuple(floors)

# not checking if all the items are still there...
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
    
    # elevator has moved to a valid floor
    # if end_e < 0 or end_e > 3:
    #     return False
    for floor in end_floors:
        if not is_valid_floor(floor):
            return False
    return True

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

# floors is a tuple of tuples. 
def get_next_states(state, lobby=False):
    floors, e = state
    next_states = []
    # assume that two different stuff cant be in elevator. 

    floors_tol = tuple([list(f) for f in floors])
    floor_contents = list(floors[e])

    for i in range(len(floor_contents)):
        # move one item. 
        floor_up = copy.deepcopy(floors_tol)
        floor_up[e].remove(floor_contents[i])
        floor_down = copy.deepcopy(floor_up)
        if (e < 3 and not lobby) or (e < 4 and lobby):
            floor_up[e+1].append(floor_contents[i])
            up_tuple = tuple([tuple(sorted(f)) for f in floor_up])
            if is_valid_move((floors, e), (up_tuple, e+1)):
                next_states.append((up_tuple, e+1))
        if e > 0:
            floor_down[e-1].append(floor_contents[i])
            down_tuple = tuple([tuple(sorted(f)) for f in floor_down])
            if is_valid_move((floors, e), (down_tuple, e-1)):
                next_states.append((down_tuple, e-1))
        
        # move two items
        for j in range(i+1, len(floor_contents)):
            floor_up = copy.deepcopy(floors_tol)
            floor_up[e].remove(floor_contents[j])
            floor_up[e].remove(floor_contents[i])
            floor_down = copy.deepcopy(floor_up)
            if (e < 3 and not lobby) or (e < 4 and lobby):
                floor_up[e+1].append(floor_contents[j])
                floor_up[e+1].append(floor_contents[i])
                up_tuple = tuple([tuple(sorted(f)) for f in floor_up])
                if is_valid_move((floors, e), (up_tuple, e+1)):
                    next_states.append((up_tuple, e+1))
            if e>0:
                floor_down[e-1].append(floor_contents[j])
                floor_down[e-1].append(floor_contents[i])
                down_tuple = tuple([tuple(sorted(f)) for f in floor_down])
                if is_valid_move((floors, e), (down_tuple, e-1)):
                    next_states.append((down_tuple, e-1))

    # print(state)
    # for s in next_states:
    #     print(s)
    # print("---")
    return next_states

seralized_dict = {}
def seralize_floors(flr):
    seen_elements = []
    new_repn = []
    for f in flr:
        this_flr = []
        for item in f:
            if item[0] not in seen_elements:
                seen_elements.append(item[0])
            index = seen_elements.index(item[0])
            this_flr.append(f"{index}{item[1]}")
        new_repn.append(tuple(sorted(this_flr)))
    return tuple(new_repn)

def get_all_perms(state, elements):
    floor, e = state
    def get_perm(serialized, p):
        new_flr = []
        for f in serialized:
            new_f = []
            for item in f:
                index = int(item[0])
                new_f.append(f"{p[index]}{item[1]}")
            new_flr.append(tuple(sorted(new_f)))
        return tuple(new_flr)

    serialized = seralize_floors(floor)
    all_permutations = list(permutations(elements))
    return [(get_perm(serialized, p), e) for p in all_permutations]

def priority_fn(state):
    floor, _ = state
    p = 1
    for i in range(len(floor)):
        p += (10**i) * len(floor[i])
    return -1*p
        
def custom_bfs(neighbor_generator, start_vertex, target=None, \
                                priorityfn=None):
    # q = [(start_vertex, 0)]
    q = PriorityQueue()
    queue_counter = 0 # pq tiebreaker. 
    q.put((1 if priorityfn is None else priorityfn(start_vertex), \
           queue_counter, start_vertex, 0))
    queue_counter += 1 
    dists = {}

    elements = get_all_elements(start_vertex[0])

    # while len(q) > 0:
    while not q.empty():
        # u, d = q.pop(0)
        _, _, u, d = q.get()

        if u in dists:
            continue

        dists[u] = d
        all_perms = get_all_perms(u, elements)
        for p in all_perms:
            if p not in dists:
                dists[p] = d

        if q.qsize() % 100 == 0:
            print(q.qsize(), d)

        if target is not None and u in get_all_perms(target, elements):
            return dists[u]
        for v in neighbor_generator(u):
            if not v in dists: #state_in_list(v, list(dists.keys()), elements):
                # q.append((v, d+1))
                q.put((1 if priorityfn is None else priorityfn(v), \
                       queue_counter, v, d+1))
                queue_counter += 1

    if target is None:
        return dists
    return -1

def p1(input):
    floors = read_input(input)
    
    all_stuff = get_all_objects(floors)
    end_list = [[], [], [], sorted(all_stuff)]
    end_position = (tuple([tuple(f) for f in end_list]), 3)
    start_position = (floors, 0)
    x = custom_bfs(get_next_states, start_position, end_position)#, priorityfn=priority_fn)#, \
                                        #    state_in_list=state_in_list)
    return x

def p2(input):
    global perms
    perms = {}

    floors = read_input(input)
    lobby = ["DG", "DM", "EG", "EM"]
    floors = tuple([tuple(sorted(f)) for f in [lobby] + list(floors)])
    
    all_stuff = get_all_objects(floors)
    end_list = [[], [], [], [], sorted(all_stuff)]
    end_position = (tuple([tuple(f) for f in end_list]), 4)
    start_position = (floors, 0)
    x = custom_bfs(get_next_states, start_position, end_position)#, \
                                        #    state_in_list=state_in_list)
    return x
