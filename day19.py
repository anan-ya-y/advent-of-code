import utils
import re # yay! back to regex! 
import operator
from functools import reduce

def get_operation(op):
    operators = {">": operator.gt, "<": operator.lt}

    sides = re.findall(r"(\w)([<>])(\d+)", op)[0]
    operation = operators[sides[1]]
    compare = sides[0]
    val = int(sides[2])
    return lambda x: operation(x[compare], val)

# for old part1
# map of {label: [operation function, state to go to]}
def parse_inst(instructions):
    states = {}

    for inst in instructions.split("\n"):
        a = re.findall(r"(\w+)\{([A-Za-z0-9>:<,]+)\}", inst)[0]
        label = a[0]
        states[label] = []
        ops = a[1].split(",")
        for op in ops:
            if ":" in op:
                # make lambda
                thing, target_label = op.split(":")
                fn = get_operation(thing)
                states[label].append((fn, target_label))
            else:
                states[label].append((lambda x: True, op))
        # print(inst, a)
    return states

# for old part1
def put_thru_map(map, state):
    current_inst_label = "in"
    # print(state)
    while current_inst_label not in ["A", "R"]:
        for inst in map[current_inst_label]:
            if inst[0](state):
                current_inst_label = inst[1]
                break
    return current_inst_label

# for p2
# {label: [(accept_intervals, target), (accept_intervals,target), ...]}
def interval_waterfall_range_creator(instructions):
    states = {}

    for inst in instructions.split("\n"):
        a = re.findall(r"(\w+)\{([A-Za-z0-9>:<,]+)\}", inst)[0]
        label = a[0]
        states[label] = []
        ops = a[1].split(",")
        for op in ops:
            accept_intervals = {
                "x": (0, 4001),
                "m": (0, 4001),
                "a": (0, 4001),
                "s": (0, 4001)
            }
            if ":" in op:
                operation, target_label = op.split(":")
                split_val = int(operation[2:])
                # if statements are wiild
                if ">" in operation:
                    accept_intervals[operation[0]] = (split_val, 4001)
                elif "<" in operation:
                    accept_intervals[operation[0]] = (0, split_val)  
                changed = operation[0]              
            else:
                target_label = op
                changed = None
            states[label].append((accept_intervals, target_label, changed))
        # print(inst, a)
    return states

# for p2
def interval_waterfall(map):
    q = []
    q.append(("in", \
              {"x":(0, 4001), \
               "m":(0, 4001), \
                "a":(0, 4001), \
                "s":(0, 4001)}
                ))
    
    accepted_ranges = []
    while len(q) > 0:
        label, ranges = q.pop(0)
        if label in "AR":
            if label == "A":
                accepted_ranges.append(ranges)
            continue

        for next_inst in map[label]:
            next_ranges, next_label, changed = next_inst
            new_ranges = ranges.copy()
            if changed is not None:
                in_range = set(range(ranges[changed][0]+1, ranges[changed][1]))
                overlap_range = set(range(next_ranges[changed][0]+1, next_ranges[changed][1]))

                new_range = in_range.intersection(overlap_range)
                remaining_range = in_range.difference(overlap_range)

                new_ranges[changed] = (min(new_range)-1, max(new_range)+1)
                ranges[changed] = (min(remaining_range)-1, max(remaining_range)+1)

            q.append((next_label, new_ranges))
    return accepted_ranges


def p1_old(input):
    instructions, states = input.split("\n\n")
    clean_states = []
    for state in states.split("\n"):
        x, m, a, s = re.findall(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)", state)[0]  
        clean_states.append({
            "x": int(x),
            "m": int(m),
            "a": int(a),
            "s": int(s)
        })

    instruction_map = parse_inst(instructions)

    sum = 0      
    for state in clean_states:
        AR = put_thru_map(instruction_map, state)
        if AR == "A":
            x, m, a, s = [state[i] for i in "xmas"]
            sum += x+m+a+s
    return sum

def p2(input):
    instructions, _ = input.split("\n\n")

    waterfall_ranges = interval_waterfall_range_creator(instructions)
    accept_intervals = interval_waterfall(waterfall_ranges)
    
    nAccept = 0
    for interval in accept_intervals:
        # What if the intervals overlap? I guess we just hope not. 
        x = interval["x"][1] - interval["x"][0] - 1
        m = interval["m"][1] - interval["m"][0] - 1
        a = interval["a"][1] - interval["a"][0] - 1
        s = interval["s"][1] - interval["s"][0] - 1
        nAccept += x*m*a*s
    return nAccept
    

def p1(input): # new, using p2. 
    instructions, states = input.split("\n\n")
    clean_states = []
    for state in states.split("\n"):
        x, m, a, s = re.findall(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)", state)[0]  
        clean_states.append(map(int, [x, m, a, s]))

    waterfall_ranges = interval_waterfall_range_creator(instructions)
    accept_intervals = interval_waterfall(waterfall_ranges)

    sum = 0
    for state in clean_states:
        x, m, a, s = state
        found = False
        for interval in accept_intervals:
            if interval["x"][0] < x < interval["x"][1] and \
                interval["m"][0] < m < interval["m"][1] and \
                interval["a"][0] < a < interval["a"][1] and \
                interval["s"][0] < s < interval["s"][1]:
                sum += (x+m+a+s)
                found = True
            if found:
                break

    return sum

