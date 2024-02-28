import utils

def p1(input):
    input = input.replace("@", ",")
    input = utils.split_and_strip(input)
    lines = [list(map(int, line.split(","))) for line in input]
    
    nIntersections = 0
    boxmin = 200000000000000
    boxmax = 400000000000000
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            x1, y1, _, vx1, vy1, _ = lines[i]
            x2, y2, _, vx2, vy2, _ = lines[j]
            if vx1/vy1 == vx2/vy2:
                continue # parallel
            x = (y2 - (vy2*x2/vx2) - y1 + (vy1*x1/vx1)) / ((vy1/vx1)-(vy2/vx2))
            y = (x - x1) * (vy1/vx1) + y1 

            if boxmin < x < boxmax and boxmin < y < boxmax:
                # check times
                tx1 = (x-x1)/vx1
                ty1 = (y-y1)/vy1
                tx2 = (x-x2)/vx2
                ty2 = (y-y2)/vy2
                if tx1>0 and tx2>0 and ty1>0 and ty2>0:
                    # print(x1, y1, x2, y2, x, y, nIntersections)
                    # print(tx1, tx2, ty1, ty2)
                    # print()
                    nIntersections += 1
    return nIntersections


def p2(input):
    input = input.replace("@", ",")
    input = utils.split_and_strip(input)
    lines = [list(map(int, line.split(","))) for line in input]
    
    import sympy as sp

    a, b, c, d, e, f = sp.symbols("a b c d e f")
    eqns = []

    for line in lines:
        x, y, z, vx, vy, vz = line
        e1 = (a-x) * (vy-e) - (b-y) * (vx-d)
        e2 = (c-z) * (vy-e) - (b-y) * (vz-f)
        eqns.append(e1)
        eqns.append(e2)

    s = sp.solve(eqns)[0]
    print(s)
    return int(s[a] + s[b] + s[c])