C = complex
import cmath, re

directions = {
    ">": C(0, 1),
    "<": C(0, -1),
    "v": C(1, 0),
    "^": C(-1, 0)
}

answer_directions = {
    directions[">"]: 0,
    directions["<"]: 2,
    directions["v"]: 1,
    directions["^"]: 3
}

def get_input(input):
    roughmap, roughinst = input.split("\n\n")

    # handle the monkey map first
    monkeymap = {}
    roughmap = roughmap.split("\n")
    nrows = len(roughmap)
    ncols = max([len(x) for x in roughmap])
    for r in range(nrows):
        for c in range(ncols):
            try:
                char = roughmap[r][c]
                if char != " ":
                    monkeymap[C(r, c)] = char
            except:
                pass

    instructions = []
    current_inst = ''
    for i in roughinst:
        if i in "RL":
            instructions.append(int(current_inst))
            instructions.append(i)
            current_inst = ''
        else:
            current_inst += i
    instructions.append(int(current_inst))

    return monkeymap, instructions

def cross_map_p1(monkeymap, current_pos, current_dir):
    if current_dir in [directions["<"], directions[">"]]:
        this_row = [x for x in monkeymap if x.real == current_pos.real]
        this_row.sort(key=lambda x: x.imag)
        if current_dir == directions[">"]:
            return this_row[0], current_dir
        else:
            return this_row[-1], current_dir
    else:
        this_col = [x for x in monkeymap if x.imag == current_pos.imag]
        this_col.sort(key=lambda x: x.real)
        if current_dir == directions["v"]:
            return this_col[0], current_dir
        else:
            return this_col[-1], current_dir
        

cube_edge_mapping = {}
def construct_cube_edge_mapping(monkeymap):
    # helper subfns
    def is_border_point(pt):
        return not (all([pt + x in monkeymap for x in directions.values()]))

    edge_length = max([x.imag+1 for x in monkeymap]) // 3
    box_toplefts = {
        1: C(0, 2*edge_length),
        2: C(0, edge_length),
        3: C(edge_length, edge_length),
        4: C(2*edge_length, edge_length),
        5: C(2*edge_length, 0), 
        6: C(3*edge_length, 0)
    }
    def get_boxnum(pt):
        for i in range(6):
            box = box_toplefts[i+1]
            if box.real <= pt.real < box.real + edge_length and \
                box.imag <= pt.imag < box.imag + edge_length:
                return i+1
        return -1

    halfmap = {}
    for pt in monkeymap:
        if not is_border_point(pt):
            continue
        
        # guaranteed to be a border point. 
        current_box_loc = get_boxnum(pt)
        assert current_box_loc != -1, "Something is wrong, line 94"
        rowdiff, coldiff = (pt - box_toplefts[current_box_loc]).real, (pt - box_toplefts[current_box_loc]).imag

        if current_box_loc == 1:
            if pt + directions["^"] not in monkeymap: # 1 to 6
                new_pos = box_toplefts[6] + C(edge_length-1, coldiff)
                new_dir = directions["^"]
                halfmap[(pt, directions["^"])] = (new_pos, new_dir)
            if pt + directions["v"] not in monkeymap: # 1 to 3
                new_pos = box_toplefts[3] + C(coldiff, rowdiff)
                new_dir = directions["<"]
                halfmap[(pt, directions["v"])] = (new_pos, new_dir)
            if pt + directions[">"] not in monkeymap: # 1 to 4
                new_pos = box_toplefts[4] + C(edge_length-1-rowdiff, coldiff)
                new_dir = directions["<"]
                halfmap[(pt, directions[">"])] = (new_pos, new_dir)

        if current_box_loc == 2:
            if pt + directions["<"] not in monkeymap: # 2 to 5
                new_pos = box_toplefts[5] + C(edge_length-1-rowdiff, coldiff)
                new_dir = directions[">"]
                halfmap[(pt, directions["<"])] = (new_pos, new_dir)

            if pt + directions["^"] not in monkeymap: # 2 to 6
                new_pos = box_toplefts[6] + C(coldiff, rowdiff)
                new_dir = directions[">"]
                halfmap[(pt, directions["^"])] = (new_pos, new_dir)

        if current_box_loc == 3:
            if pt + directions["<"] in monkeymap:
                continue
            new_pos = box_toplefts[5] + C(coldiff, rowdiff)
            new_dir = directions["v"]
            halfmap[(pt, directions["<"])] = (new_pos, new_dir)

        if current_box_loc == 4:
            if pt + directions["v"] in monkeymap:
                continue
            new_pos = box_toplefts[6] + C(coldiff, edge_length-1)
            new_dir = directions["<"]
            halfmap[(pt, directions["v"])] = (new_pos, new_dir)


        if current_box_loc in [5, 6]: # we'll flip later to get these cases. 
            continue

    for key in halfmap:
        value = halfmap[key]
        coord1, dir1 = key
        coord2, dir2 = value

        cube_edge_mapping[key] = value
        cube_edge_mapping[(coord2, -dir2)] = (coord1, -dir1)

def cross_map_p2(monkeymap, current_pos, current_dir):
    if len(cube_edge_mapping) != 0:
        return cube_edge_mapping[(current_pos, current_dir)]
    construct_cube_edge_mapping(monkeymap)
    return cross_map_p2(monkeymap, current_pos, current_dir)

def follow_inst(monkeymap, current_pos, current_dir, inst, part):
    if inst == "L":
        new_dir = current_dir * 1j
        new_pos = current_pos
    elif inst == "R":
        new_dir = current_dir * -1j
        new_pos = current_pos

    elif type(inst) == int:
        new_pos = current_pos
        new_dir = current_dir
        for i in range(inst):
            temp_pos = new_pos + new_dir
            temp_dir = new_dir
            if temp_pos not in monkeymap: # cross the map to the other side
                if part==1:
                    temp_pos, temp_dir = cross_map_p1(monkeymap, new_pos, new_dir)
                else:
                    temp_pos, temp_dir = cross_map_p2(monkeymap, new_pos, new_dir)

            if monkeymap[temp_pos] == "#": # we hit a wall
                break
        
            new_pos = temp_pos
            new_dir = temp_dir


    new_dir = C(int(new_dir.real), int(new_dir.imag))
    return new_pos, new_dir

def get_password(current_pos, current_dir):
    row = current_pos.real + 1
    col = current_pos.imag + 1
    facing = answer_directions[current_dir]
    return 1000*row + 4*col + facing


def p1(input):
    monkeymap, inst = get_input(input)

    top_row = [x for x in monkeymap if x.real == 0]
    top_row.sort(key=lambda x: x.imag)
    current_pos = top_row[0]

    current_dir = directions[">"]

    for i in range(0, len(inst)):
        current_pos, current_dir = follow_inst(monkeymap, current_pos, current_dir, inst[i], part=1)
        # print(current_pos, [x for x in directions if directions[x] == current_dir][0])

    return get_password(current_pos, current_dir)

def p2(input):
    monkeymap, inst = get_input(input)

    top_row = [x for x in monkeymap if x.real == 0]
    top_row.sort(key=lambda x: x.imag)
    current_pos = top_row[0]

    current_dir = directions[">"]

    for i in range(0, len(inst)):
        current_pos, current_dir = follow_inst(monkeymap, current_pos, current_dir, inst[i], part=2)
        # print(current_pos, [x for x in directions if directions[x] == current_dir][0])

    return get_password(current_pos, current_dir)
