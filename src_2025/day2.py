import utils

def is_valid_p1(n):
    strn = str(n)
    # if n has an odd # of digits, it's valid
    if len(strn) % 2 == 1:
        return True
    return not strn[:len(strn)//2] == strn[len(strn)//2:]

def is_valid_p2(n):
    length = len(str(n))
    strn = str(n)

    for substr_len in range(1, length):
        if length % substr_len != 0:
            continue

        multiplier = length // substr_len
        if strn[:substr_len] * multiplier == strn:
            return False
    return True

def main(input):
    inputs = utils.split_and_strip(input, ",")
    ranges = [i.split("-") for i in inputs]
    ranges = [(int(i[0]), int(i[1])) for i in ranges]

    p1 = 0
    p2 = 0
    for a, b in ranges:
        for n in range(a, b+1):
            v1 = is_valid_p1(n)
            if not v1:
                p1 += n

            v2 = is_valid_p2(n)
            if not v2:
                p2 += n

    return p1 , p2