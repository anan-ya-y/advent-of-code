c = complex
import utils


def parse_input(input):
    input = utils.split_and_strip(input)
    space = {}
    for r in range(len(input)):
        for col in range(len(input[r])):
            char = input[r][col]
            if char not in space:
                space[char] = []
            space[char].append(c(r, col))
    return space

def get_antinodes(positions, max_r, max_c):
    def is_valid_antinode(position):
        return position.real >= 0 and position.real < max_r and \
               position.imag >= 0 and position.imag < max_c
    antinodes_p1 = set()
    antinodes_p2 = set()
    for a in range(len(positions)):
        for b in range(a+1, len(positions)):
            p1 = positions[a]
            p2 = positions[b]
            diff = p2 - p1
            a_p1 = [p1-diff, p2+diff]
            a_p1 = [x for x in a_p1 if is_valid_antinode(x)]
            
            # do the part 2 antinodes
            a_p2 = [p1 - k * diff for k in range(1, max_r)] + \
                    [p2 + k * diff for k in range(1, max_r)]
            a_p2 = [x for x in a_p2 if is_valid_antinode(x)]
            a_p2 += [p1, p2]

            antinodes_p1 = antinodes_p1.union(set(a_p1))
            antinodes_p2 = antinodes_p2.union(set(a_p2))
    return antinodes_p1, antinodes_p2
    
def print_map(space, antinodes):
    max_r = int(max([p.real for p in space['.']]))+1
    max_c = int(max([p.imag for p in space['.']]))+1
    for r in range(max_r):
        for col in range(max_c):
            pos = c(r, col)
            if pos in antinodes:
                print("#", end="")
            else:
                print(".", end="")
        print()

def main(input):
    space = utils.get_complex_space(input, "values") #parse_input(input)
    max_r = int(max([p.real for p in space['.']]))+1
    max_c = int(max([p.imag for p in space['.']]))+1

    antinodes_p1 = set()
    antinodes_p2 = set()
    for k in space.keys():
        if k == ".":
            continue
        a1, a2 = get_antinodes(space[k], max_r, max_c)
        antinodes_p1 = antinodes_p1.union(a1)
        antinodes_p2 = antinodes_p2.union(a2)
    print_map(space, antinodes_p2)

    return len(antinodes_p1), len(antinodes_p2)

