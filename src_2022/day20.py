import utils, re

# def mix(input):
#     new_arr = list(enumerate(input))

#     # do it the brute force way, and come back and do it fancy
#     for i in range(len(input)):
#         # find the ith element in new_arr
#         j = [x for x in new_arr if x[0] == i][0]
#         if j[1] == 0:
#             continue



#     return new_arr


def p1(input):
    input = utils.split_and_strip(input)
    input = [int(x) for x in input]

    input = [3, 1, 0]

    new_arr = list(enumerate(input))
    def get_item(n):
        zero_index = [i for i in range(len(new_arr)) if new_arr[i][1] == 0][0]
        val = new_arr[(n + zero_index) % len(new_arr)][1]
        return val
    # position, value

    for i in range(len(input)):
        # find the ith element in new_arr
        j = [x for x in new_arr if x[0] == i][0]
        if j[1] == 0:
            continue
        # find the index of the element in input
        k = new_arr.index(j)

        if j[1] < len(new_arr): # up to single wraparound
            # shift element by that much
            new_index = k + j[1]
            if new_index <= 0:
                new_index -= 1
            if new_index >= len(input):
                new_index += 1
            new_index = new_index % len(input)
            new_arr.insert(new_index, new_arr.pop(k))
        else:
            new_index = k + j[1]
            new_index = new_index % (len(input)-1)
            new_arr.insert(new_index, new_arr.pop(k))

        print(j, new_arr)

    # new_arr = mix(input)
    print(get_item(1000))
    print(get_item(2000))
    print(get_item(3000))
    return get_item(1000) + get_item(2000) + get_item(3000)

def p2(input):
    return 1
