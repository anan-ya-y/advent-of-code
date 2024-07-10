import utils

c = complex

inst = {
    "forward": c(1, 0), 
    "down": c(0, 1),
    "up": c(0, -1),
}

inst2 = {
    "forward": lambda p, x: [p[0] + x, p[1] + (p[2]*x), p[2]], 
    "down": lambda p, x: [p[0], p[1], p[2] + x],
    "up": lambda p, x: [p[0], p[1], p[2] - x]
}

def main(input):
    input = utils.split_and_strip(input)

    pos1 = c(0, 0)
    pos2 = [0, 0, 0]
    for line in input:
        l = line.split()
        pos1 += inst[l[0]] * int(l[1])
        pos2 = inst2[l[0]](pos2, int(l[1]))

    return int(abs(pos1.real) * abs(pos1.imag)), pos2[0] * pos2[1]