import utils, re
c = complex

DIRECTIONS = [c(0, 1), c(1, 0), c(0, -1), c(-1, 0)]
SAMPLE=False
BOUNDS = 6 if SAMPLE else 70

def neighbor_fn(node, fb_set):
    n, path = node
    nbrs = []
    for d in DIRECTIONS:
        new_n = n + d
        if new_n in fb_set:
            continue
        if new_n.real > BOUNDS or new_n.real < 0 or \
            new_n.imag > BOUNDS or new_n.imag < 0:
            continue
        nbrs.append(new_n)
    return nbrs

def parse_input(inp):
    lines = utils.split_and_strip(inp)
    positions = []
    for line in lines:
        nums = list(map(int, re.findall(r'\d+', line)))
        positions.append(c(*nums))
    return positions

def print_map():
    for i in range(BOUNDS+1):
        for j in range(BOUNDS+1):
            if c(i, j) in fallen_bytes:
                print('#', end='')
            else:
                print('.', end='')
        print()

def main(inp):
    inp = parse_input(inp)
    START = c(BOUNDS, BOUNDS)
    END = c(0, 0)

    # brute force method. 
    # fallen_bytes = set()
    # for i in range(len(inp)):
    #     if i < len(inp):
    #         fallen_bytes.add(inp[i])
    #     pathlen = utils.bfs_with_neighbor_generator(lambda x: neighbor_fn(x, fallen_bytes), START, END)
    #     print(i, pathlen, inp[i])
    #     if i == (12 if SAMPLE else 1024):
    #         p1_ans = pathlen
    #     if pathlen == -1:
    #         return p1_ans, f"{int(inp[i].real)},{int(inp[i].imag)}"
    # exit()
    
    fallen_bytes = set(inp[:12 if SAMPLE else 1024])
    p1_ans = utils.bfs_with_neighbor_generator(lambda x: neighbor_fn(x, fallen_bytes), START, END)

    # binary search on the fallen_bytes array. 
    # copilot wrote the guts of the logic below :(
    low, high = 0, len(inp)
    while low < high:
        mid = (low + high) // 2
        fallen_bytes = set(inp[:mid])
        pathlen = utils.bfs_with_neighbor_generator(lambda x: neighbor_fn(x, fallen_bytes), START, END)
        if pathlen == -1:
            high = mid
        else:
            low = mid + 1
        

    return p1_ans, f"{int(inp[high-1].real)},{int(inp[high-1].imag)}"