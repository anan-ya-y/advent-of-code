import utils
C = complex

def move(pos, direction, instruction):
    if instruction[0] == 'R':
        direction *= 1j
    elif instruction[0] == 'L':
        direction *= -1j
    return pos + (direction * int(instruction[1:])), direction

def p1(input):
    input = utils.split_and_strip(input, ", ")
    pos = C(0, 0)
    direction = 1
    for instruction in input:
        pos, direction = move(pos, direction, instruction)

    return int(abs(pos.real) + abs(pos.imag))

def p2(input):
    input = utils.split_and_strip(input, ", ")
    pos = C(0, 0)
    direction = 1
    visited = set()
    doublevisited = False
    while not doublevisited:
        for instruction in input:
            pos, direction = \
                    move(pos, direction, instruction[0]+"0")
            if doublevisited:
                break
            for i in range(0, int(instruction[1:])):
                pos, direction = \
                     move(pos, direction, "S1")
                if pos in visited:
                    doublevisited = True
                    break
                visited.add(pos)
    return int(abs(pos.real) + abs(pos.imag))