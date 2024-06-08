import utils, re
import numpy as np

def p1(input):
    input = utils.split_and_strip(input)
    ans = ""
    for i in range(len(input[0])):
        chars = [x[i] for x in input]
        max_char = utils.get_n_most_frequent(chars, 1)[0][0]
        ans += max_char
    return ans

def p2(input):
    input = utils.split_and_strip(input)
    ans = ""
    for i in range(len(input[0])):
        chars = [x[i] for x in input]
        max_char = utils.get_frequencies(chars)
        min_freq = min(max_char.values())
        max_char = [c for c, f in max_char.items() if f == min_freq][0]
        ans += max_char
    return ans
