import utils 
import numpy as np

def main(input):
    input = utils.split_and_strip(input)

    gamma = 0
    eps = 0
    co2 = input
    o2  = input

    for i in range(len(input[0])):
        s = sum([int(k[i]) for k in input])

        most = 1 if s >= len(input)/2 else 0
        least = not most

        gamma <<= 1
        gamma += most

        eps <<= 1
        eps += least

        o2_most = 1 if sum([int(k[i]) for k in o2]) >= len(o2)/2 else 0
        o2 = [k for k in o2 if int(k[i]) == o2_most]

        if len(co2) != 1:
            co2_least = 1 if sum([int(k[i]) for k in co2]) < len(co2)/2 else 0
            co2 = [k for k in co2 if int(k[i]) == co2_least]

    return gamma*eps, int(o2[0], 2) * int(co2[0], 2)