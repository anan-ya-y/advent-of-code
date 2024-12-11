import utils

def one_step_one_num(num):
    if num == 0:
        return [1]
    if len(str(num)) % 2 == 0:
        chars_each = len(str(num)) // 2
        return [int(str(num)[:chars_each]), int(str(num)[chars_each:])]
    return [num * 2024]

def one_step(nums):
    new_nums = []
    for num in nums:
        new_nums += one_step_one_num(num)
    return new_nums

def one_step_with_dict(nums):
    new_nums = {}

    for num in nums:
        if num == 0:
            if 1 not in new_nums:
                new_nums[1] = 0
            new_nums[1] += nums[num]
        elif len(str(num)) % 2 == 0:
            chars_each = len(str(num)) // 2
            new_vals = [int(str(num)[:chars_each]), int(str(num)[chars_each:])]
            for val in new_vals:
                if val not in new_nums:
                    new_nums[val] = 0
                new_nums[val] += nums[num]
        else:
            if num * 2024 not in new_nums:
                new_nums[num * 2024] = 0
            new_nums[num * 2024] = nums[num]

    return new_nums


def make_cache(nepochs):
    cache = {}
    nums_to_cache = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in nums_to_cache:
        cache[i] = [i]
        arr = {i: 1}
        for _ in range(nepochs):
            arr = one_step_with_dict(arr)
            cache[i].append(sum(arr.values()))


        # cache[i] = [i]
        # arr = [i]
        # for _ in range(nepochs):
        #     arr = one_step(arr)
        #     cache[i].append(len(arr))
    return cache
    

def get_nexpanded(num, cache, nsteps):
    if nsteps == 0:
        return 1
    if num in cache and nsteps < len(cache[num]):
        return cache[num][nsteps]
    ans = 0
    for n in one_step_one_num(num):
        ans += get_nexpanded(n, cache, nsteps-1)
    return ans

def main(input):
    input = utils.split_and_strip(input, " ")
    input = list(map(int, input))

    NSTEPS_P1 = 25
    NSTEPS_P2 = 75  

    cache = make_cache(max(NSTEPS_P1, NSTEPS_P2))

    p1 = 0
    p2 = 0
    for num in input:
        p1 += get_nexpanded(num, cache, 25)
        p2 += get_nexpanded(num, cache, 75)
        
    return p1, p2

