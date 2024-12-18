import utils
import numpy as np
c = complex
DIRECTIONS = {
    ">": [0, 1], 
    "<": [0, -1],
    "^": [-1, 0],
    "v": [1, 0]
}

def parse_input(inp_map, part):
    inp_map = utils.split_and_strip(inp_map)
    length = len(inp_map)
    width = len(inp_map[0])
    map_arr = []
    robot_pos = (-1, -1)

    for row in range(length):
        r = []
        for col in range(width):
            chr = inp_map[row][col]

            if part == 1:
                r.append(chr)

            if part == 2:
                if chr in "#.":
                    r.append(chr)
                    r.append(chr)
                if chr == "O":
                    r.append("[")
                    r.append("]")
                if chr == "@":
                    r.append(".")
                    r.append(".")

            if chr == "@":
                robot_pos = (row, col*part)
                r[-1] = "."

        map_arr.append(r)

    map_arr = np.array(map_arr)
    return map_arr, robot_pos

def get_all_infront(map_arr, pos, direction):
    if direction == [0, 1]:
        position_range = range(pos[1], map_arr.shape[1])
        return ([pos[0] for _ in position_range], position_range)
    if direction == [0, -1]:
        position_range = range(pos[1], -1, -1)
        return ([pos[0] for _ in position_range], position_range)
    if direction == [1, 0]:
        position_range = range(pos[0], map_arr.shape[0])
        return (position_range, [pos[1] for _ in position_range])
    if direction == [-1, 0]:
        position_range = range(pos[0], -1, -1)
        return (position_range, [pos[1] for _ in position_range])

def one_step_p1(map_arr, robot_pos, dir_str):
    direction = DIRECTIONS[dir_str]
    new_pos = (robot_pos[0] + direction[0], robot_pos[1] + direction[1])
    # if just regular, update map. 
    if map_arr[new_pos] == ".":
        return map_arr, new_pos
    # if move into wall, do nothing. 
    if map_arr[new_pos] == "#":
        return map_arr, robot_pos
    
    # if any boxes in the way, push all boxes. 
    # map_arr[new_pos] == "O":
    forward_positions = get_all_infront(map_arr, new_pos, direction)
    forward_symbols = "".join(list(map_arr[forward_positions]))
    ntouching_boxes = len(forward_symbols) - len(forward_symbols.lstrip("O"))
    next_symbol = forward_symbols[ntouching_boxes]
    if next_symbol == "#":
        return map_arr, robot_pos
    new_fwd_symbols = "." + forward_symbols[:ntouching_boxes] + forward_symbols[ntouching_boxes+1:]
    map_arr[forward_positions] = list(new_fwd_symbols)
    return map_arr, new_pos


def one_step_p2(map_arr, robot_pos, dir_str):
    direction = DIRECTIONS[dir_str]
    new_pos = (robot_pos[0] + direction[0], robot_pos[1] + direction[1])
    # if just regular, update map. 
    if map_arr[new_pos] == ".":
        return map_arr, new_pos
    # if move into wall, do nothing. 
    if map_arr[new_pos] == "#":
        return map_arr, robot_pos
    
    # if any boxes in the way, push all boxes. 
    # map_arr[new_pos] in "[]". 
    if dir_str == "^": # going vertical up
        # THIS ENTIRE SECTION IS WRONG JUST BC I MISUNDERSTOOD IT. 
        vertical_rng = []
        for v in range(robot_pos[0]-1, -1, -1):
            vertical_rng += [v, v]
        horizontal_rng1 = robot_pos[1]
        if map_arr[new_pos] == "[":
            horizontal_rng2 = robot_pos[1]+1
        else:
            horizontal_rng2 = robot_pos[1]-1
        horizontal_rng = []
        while len(horizontal_rng) != len(vertical_rng):
            horizontal_rng += [horizontal_rng1, horizontal_rng2]
        forward_items = map_arr[vertical_rng, horizontal_rng]
        forward_symbols = "".join(forward_items)
        ntouching_boxes = 2* (len(forward_symbols) - len(forward_symbols.lstrip(forward_symbols[:1])))
        next_symbol = forward_symbols[ntouching_boxes:ntouching_boxes+2]
        if next_symbol != "..": # this includes the broken boxes []
            return map_arr, robot_pos
        new_fwd_symbols = ".." + forward_symbols[:ntouching_boxes] + forward_symbols[ntouching_boxes+2:]
        map_arr[vertical_rng, horizontal_rng] = list(new_fwd_symbols)
        return map_arr, new_pos
        
    else: # going horizontal
        forward_positions = get_all_infront(map_arr, new_pos, direction)
        forward_symbols = "".join(list(map_arr[forward_positions]))
        if direction[1] < 0: # since the string is reversed!!! 
            ntouching_boxes = len(forward_symbols) - len(forward_symbols.lstrip("]["))
        else: 
            ntouching_boxes = len(forward_symbols) - len(forward_symbols.lstrip("[]"))
        next_symbol = forward_symbols[ntouching_boxes]
        if next_symbol == "#":
            return map_arr, robot_pos
        new_fwd_symbols = "." + forward_symbols[:ntouching_boxes] + forward_symbols[ntouching_boxes+1:]
        map_arr[forward_positions] = list(new_fwd_symbols)
        return map_arr, new_pos


def print_map(map_arr, robot_pos):
    full_str = ""
    for row in range(len(map_arr)):
        for col in range(len(map_arr[0])):
            if (row, col) == robot_pos:
                full_str += "@"
            else:
                full_str += map_arr[row][col]
        full_str += "\n"
    print(full_str)
    return full_str


def main(inp):
    inp = utils.split_and_strip(inp, "\n\n")
    inp_directions = "".join(utils.split_and_strip(inp[1], "\n"))

    # PART 1
    map_arr, robot_pos = parse_input(inp[0], part=1)

    for chr in inp_directions:
        map_arr, robot_pos = one_step_p1(map_arr, robot_pos, chr)
    map_str = print_map(map_arr, robot_pos)

    box_positions = utils.get_complex_space(map_str, keys="values")["O"]

    # PART 2
    map_arr, robot_pos = parse_input(inp[0], part=2)
    print_map(map_arr, robot_pos)
    for chr in inp_directions:
        map_arr, robot_pos = one_step_p2(map_arr, robot_pos, chr)
        print(f"step {chr}")
        map_str = print_map(map_arr, robot_pos)


    return 100 * sum([x.real for x in box_positions]) + sum([x.imag for x in box_positions]), -1








