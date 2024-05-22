import utils

# returns the number of ways you can store total_amt with sizes in list. 
def nways(total_amt, container_sizes):
    print(total_amt, container_sizes)
    if total_amt <= 0:
        return frozenset()
    all_ways = set()
    for i in range(len(container_sizes)):
        enind, c = container_sizes[i]
        to_add = frozenset([(enind, c)])
        if c == total_amt:
            all_ways.add(to_add)
        if c < total_amt:
            ways = nways(total_amt-c, container_sizes[:i] + container_sizes[i+1:])
            for x in ways:
                all_ways.add(x.union(to_add))
            # all_ways.add([x.union(to_add) for x in ways ])

    return all_ways


ways = []
def p1(input):
    global ways
    input = list(map(int, utils.split_and_strip(input)))

    # input = [20, 15, 10, 5, 5]
    target = 150
    # x = nways(150, input)
    # return len(x)
    for i in range(2**len(input)):
        sum = 0
        j = i
        nshifts = 0
        while j > 0:
            if j % 2 == 1:
                sum += input[nshifts]
            j = j >> 1
            nshifts += 1
        if sum == target:
            ways.append(i)

    return len(ways)

def p2(input):
    global ways

    def count_bits(x):
        count = 0
        while x > 0:
            if x % 2 == 1:
                count += 1
            x >>= 1
        return count
    
    counts = [count_bits(w) for w in ways]
    return counts.count(min(counts))
    