import utils

def is_in_range(val, range):
    return val >= range[0] and val <= range[1]

def p1(input):
    input = utils.split_and_strip(input, '\n\n')
    ranges = utils.split_and_strip(input[0])
    vals = utils.split_and_strip(input[1])

    ranges = [tuple(map(int, r.split('-'))) for r in ranges]
    vals = [int(v) for v in vals]

    p1 = 0
    for v in vals:
        is_fresh = False
        for r in ranges:
            is_fresh |= is_in_range(v, r)
            if is_fresh:
                p1 += 1
                break

    return p1

def p2(input):
    input = utils.split_and_strip(input, '\n\n')
    ranges = utils.split_and_strip(input[0])
    ranges = [tuple(map(int, r.split('-'))) for r in ranges]

    # sort the ranges by first entry
    ranges.sort(key=lambda x: x[0])

    i = 0
    while i < len(ranges)-1:
        current = ranges[i]
        next = ranges[i+1]
        # if the two ranges are next to each other
        if current[1] == next[0] - 1:
            ranges[i] = (current[0], next[1])
            ranges.pop(i+1)

        # overlap
        elif current[0] <= next[0] <= current[1]:
            ranges[i] = (current[0], max(current[1], next[1]))
            ranges.pop(i+1)

        else:
            i += 1


    p2 = 0
    for r in ranges:
        p2 += (1 + r[1] - r[0])

    return p2