import utils, re

def process_input(input):
    lines = input.split("\n\n")
    conversions = utils.split_and_strip(lines[0])
    # all_conversions = {}
    all_conversions = []
    for c in conversions:
        r = re.findall(r"(\w+) => (\w+)", c)[0]
        all_conversions.append(r)

    return all_conversions, lines[1]

def get_replacement_indices(key, input):
    return [m.start() for m in re.finditer('(?=' + key + ')', input)]

def get_possible_onesteps(input_str, convs):
    possible_strings = set()
    for c in convs:
        key, val = c
        occurrences = get_replacement_indices(key, input_str)
        for o in occurrences:
            new_val = input_str[:o]+input_str[o:].replace(key, val, 1)
            possible_strings.add(new_val)
    return list(possible_strings)


def p1(input):
    convs, input_str = process_input(input)
    return len(get_possible_onesteps(input_str, convs))

def p2(input):
    convs, input_str = process_input(input)
    def neighbor_generator(u):
        return get_possible_onesteps(u, convs)
    # return utils.bfs_with_neighbor_generator(neighbor_generator, "e", input_str)

    reverse_convs = [(v, u) for (u, v) in convs]

    def neighbor_generator_reverse(u):
        return get_possible_onesteps(u, reverse_convs)
    
    k = utils.bfs_with_neighbor_generator(neighbor_generator_reverse, input_str, "e")
    return k 