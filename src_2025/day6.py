import utils
import numpy as np
import re
from operator import add, mul
from functools import reduce


def preprocess(input):
    input = utils.split_and_strip(input)
    numbers = input[:-1]
    operations = input[-1]
    operations = [ o for o in re.split(r"\s", operations) if o != '']

    numbers = [re.split(r"\s", n) for n in numbers]
    numbers = [
        [int(x) for x in n if x != ""]
        for n in numbers
    ]

    numbers = np.array(numbers).T
    return numbers, operations

def do_math(nums, ops):
    ans = 0
    for net, operator in zip(nums, ops):
        if operator == "+":
            ans += reduce(add, net)
        else:
            ans += reduce(mul, net)
    return ans

def p1(input):
    numbers, operations = preprocess(input)
    return do_math(numbers, operations)

def p2(input):
    input = input.split("\n")
    input = [i + " " for i in input]
    numbers = []
    op = ""
    ans = 0
    for i in range(len(input[0])):
        digits = [x[i] for x in input]
        if all([d==' ' for d in digits]):
            ans += do_math([numbers], [op.strip()])
            numbers = []
            op = ""
            continue

        op += digits[-1]

        numbers.append(int("".join(digits[:-1]).strip()))

    return ans


