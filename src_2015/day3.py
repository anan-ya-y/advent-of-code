C = complex

directions = {
    ">": C(0, 1),
    "<": C(0, -1),
    "v": C(1, 0),
    "^": C(-1, 0), 
}

def p1(input):
    pos = C(0, 0)
    seen_houses = set([pos])
    for i in input:
        pos += directions[i]
        seen_houses.add(pos)
    return len(seen_houses)

def p2(input):
    pos = C(0, 0)
    robopos = C(0, 0)
    seen_houses = set([pos])
    for i in range(0, len(input), 2):
        pos += directions[input[i]]
        robopos += directions[input[i+1]]
        seen_houses.add(pos)
        seen_houses.add(robopos)
    return len(seen_houses)

