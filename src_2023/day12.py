# I REALLY REALLY DID NOT FEEL LIKE DOING THIS ONE. 
# So, I looked online, wrote the recurrence on paper, and then wrote this. 
# https://github.com/Anshuman-UCSB/Advent-Of-Code/blob/master/2023/Python/src/day12.py
import utils

def get_n_arrangements(arr, nums):
    arrangements = {}
    # Not gonna care about eval order. 
    # number of possible arrangements of nums[j:] in arr[i:] given 
    # that we have arranged b entries of nums[j]. 
    def arrange(i, j, b): 
        if (i, j, b) in arrangements:
            return arrangements[(i, j, b)]
        
        if i >= len(arr):
            nways = 0
            if j >= len(nums) and b == 0:
                nways = 1
            if j == len(nums)-1 and b == nums[-1]:
                nways = 1
            arrangements[(i, j, b)] = nways
            return nways
            
        
        nways = 0
        if arr[i] in "?.": # this is a .
            if b == 0:
                nways += arrange(i+1, j, 0) # just a dot
            else:
                if j >= len(nums): 
                    # we are partly thorugh a list of springs but we don't want any more springs
                    arrangements[(i, j, b)] = 0
                    return 0
                if b == nums[j]:
                    nways += arrange(i+1, j+1, 0) # finish this operation
                if b < nums[j]:
                    nways += 0 # broke the dot


        if arr[i] in "?#": # this is a #
            # advance the current arrangement
            nways += arrange(i+1, j, b+1)

        arrangements[(i, j, b)] = nways
        return nways
        
    return arrange(0, 0, 0)

def p1(input):
    input = utils.split_and_strip(input)

    sum = 0
    for i in input:
        springlist, nums = i.split(" ")
        nums = list(map(int, nums.split(",")))

        sum += get_n_arrangements(springlist, nums)

    return sum

def p2(input):
    input = utils.split_and_strip(input)

    sum = 0
    for i in input:
        springlist, nums = i.split(" ")
        nums = list(map(int, nums.split(",")))

        sum += get_n_arrangements("?".join([springlist]*5), nums*5)

    return sum