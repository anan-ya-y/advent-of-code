import utils

def parse_instruction(inst):
    parts = inst.split(": ")
    dims = list(map(int, parts[0].split("x")))

    counts = list(map(int, parts[1].split(" ")))

    return dims[0], dims[1], counts

# the dumb way works? whoa
def p1(inp):
    inp = utils.split_and_strip(inp, '\n\n')
    instructions = utils.split_and_strip(inp[-1])
    shape_sizes = [x.count("#") for x in inp[:-1]]
    instructions = [parse_instruction(inst) for inst in instructions]


    ans = 0
    for inst in instructions:
        x, y, counts = inst
        total_slots = x * y
        used_slots = sum([a*b for a, b in zip(shape_sizes, counts)])

        ans += used_slots <= total_slots

    return ans
