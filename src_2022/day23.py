import re, utils
C = complex
N = C(0, -1)
S = C(0, 1)
E = C(-1, 0)
W = C(1, 0)

def get_elf_locations(input):
    input = input.split('\n')
    elf_locations = set()
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == '#':
                elf_locations.add(C(x, y))
    return elf_locations

def show_grid(elf_locs, boundsx=-1, boundsy=-1):
    max_x = int(max([x.real for x in elf_locs])) if boundsx == -1 else boundsx
    max_y = int(max([x.imag for x in elf_locs])) if boundsy == -1 else boundsy

    for y in range(max_y+1):
        for x in range(max_x+1):
            if C(x, y) in elf_locs:
                print('#', end='')
            else:
                print('.', end='')
        print()
    


def first_half(elf_locs, round_num):
    new_elf_locs = {} # new_elf_loc: [original_elf_loc]
    all_dirs = [N, S, E, W, N + E, N + W, S + E, S + W] 
    direction_candidates = [
        ([N, N + E, N + W], N), 
        ([S, S + E, S + W], S), 
        ([E, N + E, S + E], E), 
        ([W, N + W, S + W], W)
    ]
    unmoving_elves_happy = set()
    unmoving_elves_sad = set()

    def elf_in_dir(elf, dirset, nextloc_if_empty):
        dirset = set(dirset)
        if dirset.intersection(elf_locs) == set():
            if nextloc_if_empty in new_elf_locs:
                new_elf_locs[nextloc_if_empty].append(elf)
            else:
                new_elf_locs[nextloc_if_empty] = [elf]
            return True
        return False
    
    # rotate the direction candidates
    direction_candidates = direction_candidates[round_num % 4:] \
                        + direction_candidates[:round_num % 4]
            

    for elf in elf_locs:
        surrounding = [d + elf for d in all_dirs]

        # no other elves surrounding
        if set(surrounding).intersection(elf_locs) == set():
            unmoving_elves_happy.add(elf)
            continue # no other elves surrounding

        moved = False
        for direction in direction_candidates:
            if not moved and \
                elf_in_dir(elf, [elf+d for d in direction[0]], elf + direction[1]):
                moved = True
            
        if not moved:
            unmoving_elves_sad.add(elf)

    return new_elf_locs, unmoving_elves_happy, unmoving_elves_sad
    
def second_half(new_elf_locs, unmoving_elves):
    all_elf_locs = unmoving_elves

    for new_loc, old_locs in new_elf_locs.items():
        if len(old_locs) > 1:
            all_elf_locs = all_elf_locs.union(set(old_locs))
            continue
        
        all_elf_locs.add(new_loc)
    
    return all_elf_locs
        
def get_area(elf_locs):
    minx = int(min([x.real for x in elf_locs]))
    maxx = int(max([x.real for x in elf_locs]))
    miny = int(min([x.imag for x in elf_locs]))
    maxy = int(max([x.imag for x in elf_locs]))

    return (maxx - minx+1) * (maxy - miny+1) - len(elf_locs)


def p1(input):
    elf_locs = get_elf_locations(input)
    nelves = len(elf_locs)
    # show_grid(elf_locs, 12, 14)

    for i in range(1, 11):
        new_elf_locs, happy_elves, sad_elves = first_half(elf_locs, i-1)
        elf_locs = second_half(new_elf_locs, happy_elves.union(sad_elves))
        assert len(elf_locs) == nelves

        # print("END OF ROUND", i)
        # show_grid(elf_locs, 12, 14)

    return get_area(elf_locs)

def p2(input):
    elf_locs = get_elf_locations(input)
    nelves = len(elf_locs)
    # show_grid(elf_locs, 12, 14)

    i = 1
    while True:
        new_elf_locs, happy_elves, sad_elves = first_half(elf_locs, i-1)

        if len(happy_elves) == nelves:
            return i
        
        elf_locs = second_half(new_elf_locs, happy_elves.union(sad_elves))
        assert len(elf_locs) == nelves

        i += 1
    