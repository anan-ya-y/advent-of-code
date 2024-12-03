import utils

def is_safe(x):
    inc = x[1] > x[0]
    for i in range(len(x)-1):
        if abs(x[i] - x[i+1]) == 0 or \
            abs(x[i] - x[i+1]) > 3:
            return False
        if inc and x[i] > x[i+1]:
            return False
        if not inc and x[i] < x[i+1]:
            return False
    return True

def main(input):
    input = utils.split_and_strip(input)
    input = [list(map(int, x.split())) for x in input]

    p1 = 0
    p2 = 0

    for i in input:
        if is_safe(i):
            p1 += 1
            p2 += 1
        else:
            for j in range(len(i)): # take out the jth element
                if is_safe(i[:j] + i[j+1:]):
                    p2 += 1
                    break

    return p1, p2


