import numpy.linalg as la
import numpy as np
import utils

# recursion >>> while loops. 
def get_next_element(arr):
    if not arr.any(): # if array is all 0s
        return 0
    d = np.diff(arr)
    return arr[-1] + get_next_element(d)


def p1(input):
    lines = utils.split_and_strip(input)
    nums = [[int(l) for l in line.split(" ")] for line in lines]
    nums = np.array(nums)
    return sum([get_next_element(l) for l in nums])

def p2(input):
    lines = utils.split_and_strip(input)
    nums = [[int(l) for l in line.split(" ")] for line in lines]
    nums = np.array(nums)
    return sum([get_next_element(l[::-1]) for l in nums])