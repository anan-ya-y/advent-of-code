import utils, re

def parse_input(input):
    input = utils.split_and_strip(input)
    rules = {} # {bot: [low, high]}
    state = {} # {bot OUR out1: [chips]}
    for line in input:
        values = re.findall(r'(bot|output|value) (\d+)', line)
        values = [v[0][0]+v[1] for v in values]
        values = [int(v[1:]) if v[0] == "v" else v for v in values]
        
        if "value" in line:
            if values[1] not in state:
                state[values[1]] = []
            state[values[1]].append(values[0])
        else:
            rules[values[0]] = values[1:]
    return rules, state

def find_bot_with_two_chips(state):
    for bot, chips in state.items():
        if len(chips) == 2:
            return bot
    return None

def pass_chips(bot, state, rules):
    low, high = rules[bot]
    chips = state[bot]

    # add bots if theyre not known by state
    if low not in state:
        state[low] = []
    if high not in state:
        state[high] = []

    # do the passing
    state[bot] = []
    state[low].append(min(chips))
    state[high].append(max(chips))
    return state

out1 = None
out2 = None
def main(input):
    rules, state = parse_input(input)
    
    out1 = None
    out2 = None

    while True:
        b = find_bot_with_two_chips(state)
        if not b:
            break

        low, high = sorted(state[b])
        if low == 17 and high == 61 and out1 is None:
            out1 = b[1:]
        state = pass_chips(b, state, rules)
    out2 = state["o0"][0] * state["o1"][0] * state["o2"][0]
    return out1, out2

def p1(input):
    global out1, out2
    out1, out2 = main(input)
    return out1
        
def p2(input):
    global out1, out2
    return out2