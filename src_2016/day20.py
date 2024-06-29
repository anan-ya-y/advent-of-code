import utils

MAXVAL = 4294967295

def clean_input(input):
    input = utils.split_and_strip(input)
    input = [x.split("-") for x in input]
    input = [tuple(map(int, x)) for x in input]
    input.sort()
    return input

def p1(input):
    input = clean_input(input)
    m = 0
    for line in input:
        start, end = line
        if m >= start:
            m = max(m, end + 1)

    return m

def p2(input):
    input = clean_input(input)
    
    all_illegal_intervals = []
    for line in input:
        start, end = line
        added = False
        for i in all_illegal_intervals:
            interval_start, interval_end = i
            if added:
                break

            if start >= interval_start and start <= interval_end:
                all_illegal_intervals.remove(i)
                new_end = max(end, interval_end)
                all_illegal_intervals.append((interval_start, new_end))
                added = True
            elif end >= interval_start and end <= interval_end:
                all_illegal_intervals.remove(i)
                new_start = min(start, interval_start)
                all_illegal_intervals.append((new_start, interval_end))
                added = True
        if not added:
            all_illegal_intervals.append((start, end))

    nfree = MAXVAL + 1
    for i in all_illegal_intervals:
        nfree -= i[1] - i[0] + 1

    return nfree