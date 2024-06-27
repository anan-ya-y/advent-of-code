import utils
C = complex
left = C(-1, -1)
right = C(-1, 1)
center = C(-1, 0)

def print_set(s, rowlen):
    for row in range(rowlen):
        for col in range(rowlen):
            if C(row, col) in s:
                print('^', end='')
            else:
                print('.', end='')
        print()

def get_num_safe_tiles(input, nrows):
    traps = set()
    rowlen = len(input)
    for i in range(rowlen):
        c = input[i]
        if c == '^':
            traps.add(C(0, i))

    for rownum in range(1, nrows): #rownum < rowlen - 1:
        # rownum += 1
        for i in range(rowlen):
            this_tile = C(rownum, i)
            
            l = this_tile + left
            r = this_tile + right
            c = this_tile + center

            if (l in traps and c in traps and r not in traps) or \
                (c in traps and r in traps and l not in traps) or \
                (l in traps and r not in traps and c not in traps) or \
                (r in traps and l not in traps and c not in traps):
                traps.add(this_tile)

    # print_set(traps, rowlen)
    return (rowlen * nrows) - len(traps)

def p1(input):
    nrows = 40
    return get_num_safe_tiles(input, nrows)


def p2(input):
    nrows = 400000
    return get_num_safe_tiles(input, nrows)
