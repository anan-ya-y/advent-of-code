import utils
from functools import reduce

sstn = {}
def subset_sum(nums, target_sum):
    if len(nums) == 0:
        return False, []
    if target_sum <= 0:
        return False, []
    n = nums[0]
    if n == target_sum:
        return True, [n]
    if sum(nums) < target_sum:
        return False, []
    
    # repn = (tuple(nums), target_sum)
    # if repn in sstn:
    #     return sstn[repn]
    
    use, use_set = subset_sum(nums[1:], target_sum - n)
    dont_use, dont_use_set = subset_sum(nums[1:], target_sum)
    use_set += [n]

    assert n not in dont_use_set, "ERROR with DP. "

    if use and dont_use:
        if len(use_set) == len(dont_use_set):
            ans = min(use_set, dont_use_set, key=lambda x: reduce(lambda a, b: a*b, x))
        else:
            ans = min(use_set, dont_use_set, key=lambda x: len(x))
    elif use and not dont_use:
        ans = use_set
    elif dont_use and not use:
        ans = dont_use_set
    else:
        # sstn[repn] = False, []
        return False, []
    
    # sstn[repn] = use or dont_use, ans
    return use or dont_use, ans

def p1(input):
    nums = list(map(int, utils.split_and_strip(input)))
    nums.sort(reverse=True)

    target_sum = sum(nums) // 3

    _, nums = subset_sum(nums, target_sum)

    return reduce(lambda x, y: x * y, nums)


def p2(input):
    nums = list(map(int, utils.split_and_strip(input)))
    nums.sort(reverse=True)
    
    target_sum = sum(nums) // 4

    _, nums = subset_sum(nums, target_sum)

    return reduce(lambda x, y: x * y, nums)