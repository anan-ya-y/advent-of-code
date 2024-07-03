import utils

def main(input):
    input = utils.split_and_strip(input)
    input = list(map(int, input))

    p1, p2 = 0, 0
    for i in range(len(input) - 1):
        if input[i+1] > input[i]:
            p1 += 1

    for i in range(len(input) - 2):
        sum1 = sum(input[i:i+3])
        sum2 = sum(input[i+1:i+4])
        if sum2 > sum1:
            p2 += 1

    return p1, p2
