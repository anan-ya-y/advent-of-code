import utils

def p1(input):
    global memo
    batts = utils.split_and_strip(input)
    # p1 = sum([get_max_possible_joltage(batt) for batt in batts])
    p1 = 0
    for batt in batts:
        memo = {}
        b = get_max_possible_remaining_joltage(batt, 0, 2)
        p1 += b

    return p1

# picks the best n joltage 
memo = {}
def get_max_possible_remaining_joltage(full_batts, startindex, n):
    global memo
    full_len = len(full_batts)
    batts = full_batts[startindex:]
    if n == 0 or batts == "":
        return 0
    
    if n == 1:
        return max([int(b) for b in batts])
    
    if len(batts) == n:
        return int(batts)
    
    if len(batts) < n:
        return 0
    
    if (startindex, n) in memo:
        return memo[(startindex, n)]
    
    best_joltage = 0
    for pos in range(len(batts)-n+1):
        val = int(batts[pos]) * (10**(n-1)) + get_max_possible_remaining_joltage(full_batts, startindex + pos + 1, n-1) 
        best_joltage = max(best_joltage, val)

    memo[(startindex, n)] = best_joltage
    return best_joltage


def p2(input):
    global memo
    batts = utils.split_and_strip(input)
    p2 = 0
    for b in batts:

        memo = {}
        j = get_max_possible_remaining_joltage(b, 0, 12)
        p2 += j

    return p2


