import re
import utils
import numpy as np

# return list (ax, ay), (bx, by), (px, py)
def parse_input(input):
    input = utils.split_and_strip(input, "\n\n")
    ans = []
    for i in range(len(input)):
        lines = utils.split_and_strip(input[i])
        l1 = tuple(map(int, re.findall(r"\d+", lines[0])))
        l2 = tuple(map(int, re.findall(r"\d+", lines[1])))
        p = tuple(map(int, re.findall(r"\d+", lines[2])))
        
        ans.append((l1, l2, p))
    return ans
        

def main(input):
    input = parse_input(input)
    
    p1 = 0
    p2 = 0
    for i in input:
        A = np.array([[i[0][0], i[1][0]], [i[0][1], i[1][1]]])
        b1 = np.array([i[2][0], i[2][1]])
        b2 = b1 + 10000000000000

        x = np.linalg.solve(A, b1)
        x = np.round(x, 0)    
        if all(b1 == A@x) and all(x >= 0) and all(x <= 100):
            p1 += x[0] * 3 + x[1]

        x = np.linalg.solve(A, b2)
        x = np.round(x, 0)
        if all(b2 == A@x):
            p2 += x[0] * 3 + x[1]       

    return p1, p2