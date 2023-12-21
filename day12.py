# I REALLY REALLY DID NOT FEEL LIKE DOING THIS ONE. 
# So, I copied someone else's. 
# I know & understand how it works, I guess, but I did not write this at all .
# https://github.com/Anshuman-UCSB/Advent-Of-Code/blob/master/2023/Python/src/day12.py

import re

def solve(line, nums, part1=True):
    if part1 == False:
        line = "?".join([line]*5)
        nums *= 5

    DP = {}

    def f(i, n, b): # return how many solutions there are from this position
        # i - index in line
        # n - index in nums
        # b - size of current block
        if (i,n,b) in DP:return DP[(i,n,b)] # DP already solved it
        
        if i == len(line):    # at the end of the line, return 1 if this is a posible configuration or 0 otherwise
            return int(
                n == len(nums) and b == 0 or             # no current block, and finished all numbers
                n == len(nums)-1 and b == nums[-1]        # one last block, and currently in a block of that size
            )

        ans = 0
        if line[i] in ".?":    # treat it like a .
            if(b == 0):
                ans += f(i+1, n, 0) # just keep moving forward
            else:            # we have a current block
                if n == len(nums): return 0    # more springs than input asks for, so not a solution
                if b == nums[n]:             # If we currently have a continguous spring of the required size
                    ans += f(i+1, n+1, 0)    # Move forward and count this block
        if line[i] in "#?": # treat it like a #
            ans += f(i+1, n, b+1)     # no choice but to continue current block
        DP[(i,n,b)] = ans # save to DP
        return ans
    return f(0,0,0)

def parseLine(l):
    lhs,rhs = re.sub(r"\.+",".",l).split()
    nums = eval(rhs)
    return (lhs, nums)

p1_ans, p2_ans = 0, 0
def main(input):
    inps = [parseLine(l) for l in input.splitlines()]
    global p1_ans, p2_ans
    p1_ans, p2_ans = sum(solve(*l) for l in inps), sum(solve(*l, part1 = False) for l in inps)

def p1(input):
    main(input)
    global p1_ans
    return p1_ans

def p2(input):
    global p2_ans
    return p2_ans