C = complex
import cmath

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

    return monkeymap, instructions

def follow_inst(monkeymap, current_pos, current_dir, inst):
    if inst == "L":
        new_dir = cmath.rect(1, cmath.phase(current_dir) + cmath.pi/2)
        new_pos = current_pos
    elif inst == "R":
        new_dir = cmath.rect(1, cmath.phase(current_dir) - cmath.pi/2)
        new_pos = current_pos

    elif type(inst) == int:
        new_pos = current_pos
        for i in range(inst):
            temp_pos = new_pos + current_dir
            if temp_pos not in monkeymap: # rotate
                if current_dir in [directions["<"], directions[">"]]:
                    this_row = [x for x in monkeymap if x.real == current_pos.real]
                    this_row.sort(key=lambda x: x.imag)
                    temp_pos = this_row[0]
                else:
                    this_col = [x for x in monkeymap if x.imag == current_pos.imag]
                    this_col.sort(key=lambda x: x.real)
                    temp_pos = this_col[0]

            if monkeymap[temp_pos] == "#": # we hit a wall
                break
        
            new_pos = temp_pos
        new_dir = current_dir

    new_dir = C(int(new_dir.real), int(new_dir.imag))
    return new_pos, new_dir

def p1(input):
    monkeymap, inst = get_input(input)

    top_row = [x for x in monkeymap if x.real == 0]
    top_row.sort(key=lambda x: x.imag)
    current_pos = top_row[0]

    current_dir = directions[">"]

    for i in range(0, len(inst)):
        current_pos, current_dir = follow_inst(monkeymap, current_pos, current_dir, inst[i])
        # print(current_dir)
        # print(current_pos, [x for x in directions if directions[x] == current_dir][0])

    row = current_pos.real + 1
    col = current_pos.imag + 1
    facing = answer_directions[current_dir]
    return 1000*row + 4*col + facing

def p2(input):
    return -1