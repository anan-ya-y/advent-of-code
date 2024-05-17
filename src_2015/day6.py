import re, utils
import numpy as np

instructions = []
def read_input(input):
    input = utils.split_and_strip(input)
    instructions = []
    for line in input:
        inst = re.findall(r'(on|off|toggle)', line)
        r = re.findall(r'\d+', line)
        r = list(map(int, r))
        instructions.append(inst+r)
    return instructions
        
def p1(input):
    global instructions
    instructions = read_input(input)
    lights = np.array([[0 for i in range(1000)] for j in range(1000)])

    for inst in instructions:
        i, x1, y1, x2, y2 = inst
        if i == "on":
            lights[x1:x2+1, y1:y2+1] = 1
        elif i == "off":
            lights[x1:x2+1, y1:y2+1] = 0
        elif i == "toggle":
            lights[x1:x2+1, y1:y2+1] = np.logical_not(lights[x1:x2+1, y1:y2+1])

    return np.sum(lights)

def p2(input):
    lights = np.array([[0 for i in range(1000)] for j in range(1000)])

    for inst in instructions:
        i, x1, y1, x2, y2 = inst
        shape = lights[x1:x2+1, y1:y2+1].shape
        if i == "on":
            lights[x1:x2+1, y1:y2+1] += 1
        elif i == "off":
            lights[x1:x2+1, y1:y2+1] = np.maximum(lights[x1:x2+1, y1:y2+1] - np.ones(shape), np.zeros(shape))
        elif i == "toggle":
            lights[x1:x2+1, y1:y2+1] += 2

    return np.sum(lights)