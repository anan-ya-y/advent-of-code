import utils

def main(inp):
    inp = utils.split_and_strip(inp)
    inp = [tuple(map(int, x.split(','))) for x in inp]

    p1 = 0
    for i in range(len(inp)):
        for j in range(i + 1, len(inp)):
            xdiff = abs(inp[i][0] - inp[j][0]) + 1
            ydiff = abs(inp[i][1] - inp[j][1]) + 1
            
            p1 = max(p1, xdiff * ydiff)

    return p1, -1