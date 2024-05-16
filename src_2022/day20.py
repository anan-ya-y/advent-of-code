import utils, re

def mix(input):
    new_arr = input.copy()

    for i in range(len(input)):
        # find this element in new_arr
        j = [x for x in new_arr if x[0] == i][0]
        if j[1] == 0:
            continue

        index = new_arr.index(j)
        slot_num = index-1
        new_slot_num = (slot_num + j[1]) % (len(input) - 1)
        new_arr.pop(index)
        new_arr.insert(new_slot_num+1, j)

    return new_arr

def get_item(new_arr, n):
    zero_index = [i for i in range(len(new_arr)) if new_arr[i][1] == 0][0]
    val = new_arr[(n + zero_index) % len(new_arr)][1]
    return val

def p1(input):
    input = utils.split_and_strip(input)
    input = [int(x) for x in input]

    new_arr = mix(list(enumerate(input)))

    x = []
    x.append(get_item(new_arr, 1000))
    x.append(get_item(new_arr, 2000))
    x.append(get_item(new_arr, 3000))

    return sum(x)

def p2(input):
    input = utils.split_and_strip(input)

    decryption_key = 811589153
    input = [int(x) * decryption_key for x in input]
    input = list(enumerate(input))

    new_arr = []
    for i in range(10):
        new_arr = mix(input)
        # input = [x[1] for x in new_arr]
        input = new_arr

    x = []
    x.append(get_item(new_arr, 1000))
    x.append(get_item(new_arr, 2000))
    x.append(get_item(new_arr, 3000))
    return sum(x)