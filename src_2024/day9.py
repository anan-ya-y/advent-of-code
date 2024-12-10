def get_index(l, n):
    for i in range(len(l)):
        if sum(l[:i]) >= n:
            return i, sum(l[:i]) - n
    return len(l)


def p1old(input):
    input = list(map(int, input))
    assert len(input) % 2 == 1
    ndots = sum(input[1::2])
    nfiles = len(input[::2])
    noccupied_slots = sum(input) - ndots

    p1_end_index, remainder = get_index(input, noccupied_slots)
    p1_arr = input[:p1_end_index]
    p1_arr[-1] -= remainder
    p1_remaining_arr =  (input[p1_end_index:])[::-2] + [remainder]
    
    forward_index = 0
    backward_index = 0
    backward_count = 0
    forward_value = 0
    backward_value = nfiles-1

    ans = 0
    position = 0
    while position < noccupied_slots:
        if forward_index % 2 == 0:
            for i in range(p1_arr[forward_index]):
                # print(forward_value, end="")
                ans += (position * forward_value)
                position += 1
            forward_value += 1
        else: # backward
            for i in range(p1_arr[forward_index]):
                # print(backward_value, end="")
                ans += (position * backward_value)
                backward_count += 1
                if backward_count == p1_remaining_arr[backward_index]:
                    backward_index += 1
                    backward_count = 0
                    backward_value -= 1
                position += 1
        forward_index += 1
    # print()
    
    return ans

def get_arr(input):
    original_arr = []
    index = 0
    for i in range(len(input)):
        for j in range(input[i]):
            if i % 2 == 0:
                original_arr.append(index)
            else:
                original_arr.append(".")
        if i % 2 == 0:
            index += 1
    return original_arr

def p1(input):
    input = list(map(int, input))
    ndots = sum(input[1::2])
    nfiles = len(input[::2])
    noccupied_slots = sum(input) - ndots
    original_arr = get_arr(input)
        
    ans_arr = original_arr[:noccupied_slots]
    reverse_arr = [x for x in (original_arr[noccupied_slots:])[::-1] if x != "."]
    for i in range(len(ans_arr)):
        if ans_arr[i] == ".":
            ans_arr[i] = reverse_arr.pop(0)
    
    return sum([i*x for i, x in enumerate(ans_arr)])

def p2(input):
    input = list(map(int, input))
    only_files = input[::2]
    file_lengths = {i: j for i, j in enumerate(only_files)}
    files_moved = set()

    arr = get_arr(input)
    
    for i in range(max(file_lengths.keys()), -1, -1):
        nfreeslots_required = file_lengths[i]
        start_position = arr.index(i)

        if nfreeslots_required == 0:
            continue

        start_dots = -1
        ndots = 0
        for j in range(len(arr)):
            if arr[j] == ".":
                if start_dots == -1:
                    start_dots = j
                ndots += 1
            elif j > start_position: # we'd be moving it forward
                start_dots = -1
                ndots = 0
                break
            else:
                if ndots >= nfreeslots_required:
                    break
                start_dots = -1
                ndots = 0
        if ndots < nfreeslots_required: # can't move this number
            continue
    
        # remove this number from the original_arr
        arr = [x if x != i else "." for x in arr]
        for j in range(start_dots, start_dots+nfreeslots_required):
            arr[j] = i
        # print(" ".join(map(str, arr[:75])))
        
    arr = [x if x != "." else 0 for x in arr]
    return sum([i*x for i, x in enumerate(arr)])
    

