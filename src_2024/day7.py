import utils

def parse_input(input):
    input = utils.split_and_strip(input)
    lines = []
    for l in input:
        target, nums = utils.split_and_strip(l, ":")
        nums = list(map(int, utils.split_and_strip(nums, " ")))
        target = int(target)
        lines.append((target, nums))
    return lines

def works(previous, remaining_nums, target, used_bars=False):
    if len(remaining_nums) == 0:
        return previous == target, used_bars
    if previous > target:
        return False, used_bars
    
    next_num = remaining_nums[0]
    next_remaining = remaining_nums[1:]

    next_options = [
        previous + next_num,
        previous * next_num,
        int ( str(previous) + str(next_num) )
    ]

    for o in range(len(next_options)):
        option = next_options[o]
        ans_acheived, bars = works(option, next_remaining, target, used_bars or (o == 2))
        if ans_acheived:
            return True, (used_bars or bars)
    return False, used_bars

def works2(previous, remaining_nums, target, part):
    if len(remaining_nums) == 0:
        return previous == target
    if previous > target:
        return False
    
    next_num = remaining_nums[0]
    next_remaining = remaining_nums[1:]

    next_nums = [
        previous + next_num,
        previous * next_num,
        int ( str(previous) + str(next_num) )
    ]

    for i in range(part+1):
        if works2(next_nums[i], next_remaining, target, part):
            return True
        
def main(input):
    items = parse_input(input)
    
    p1 = 0
    p2 = 0
    for item in items:
        target, nums = item
        reached, used_bars = works(nums[0], nums[1:], target)
        if reached and not used_bars:
            p1 += target
        p2 += (target * reached)
        # if works2(nums[0], nums[1:], target, 1):
        #     p1 += target
        #     p2 += target
        # elif works2(nums[0], nums[1:], target, 2):
        #     p2 += target

    return p1, p2
