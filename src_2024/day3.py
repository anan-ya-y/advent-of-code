import utils
import re

def main(input):
    # mul_pairs = re.findall(r"mul\((\d+),(\d+)\)", input)
    mul_dodont_pairs = re.findall(r"mul\((\d+),(\d+)\)|(do|don't)\(\)", input)
    # p1 = sum([int(x)*int(y) for x, y in mul_pairs])
    p1 = 0
    p2 = 0
    enabled=True
    for x, y, do in mul_dodont_pairs:
        if x.isnumeric(): # this is a mul 
            product = int(x)*int(y)
            p1 += product
            p2 += product if enabled else 0
        else: # this is a do or don't
            enabled = (do == "do")

    return p1, p2