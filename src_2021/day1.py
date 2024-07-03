import utils

def main(input):
    input = utils.split_and_strip(input)
    input = list(map(int, input))

    p1, p2 = 0, 0
    for i in range(len(input) - 1):
        if input[i+1] > input[i]:
            p1 += 1

    return p1, p2
