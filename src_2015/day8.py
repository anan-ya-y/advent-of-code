import re, utils

def p1(input):
    input = utils.split_and_strip(input)
    return sum(len(code) - len(eval(code)) for code in input)

def p2(input):
    input = utils.split_and_strip(input)
    s = 0
    for code in input:
        s += code.count('\\') + code.count('"') + 2 + len(code)
    return s - sum(len(code) for code in input)