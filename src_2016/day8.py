import utils
import numpy as np

def read_input(input):
    input = utils.split_and_strip(input)
    instructions = []
    for line in input:
        if line.startswith("rect"):
            x, y = map(int, line.split()[1].split("x"))
            instructions.append(("rect", x, y))
        else:
            _, inst, y, _, amount = line.split()
            y = int(y.split("=")[1])
            amount = int(amount)
            instructions.append((inst, y, amount))

    return instructions

def apply_rect(screen, x, y):
    screen[:y, :x] = "#"
    return screen

def apply_row(screen, y, amt):
    y %= len(screen)
    screen[y] = np.roll(screen[y], amt)
    return screen

def apply_col(screen, x, amt):
    x %= len(screen[0])
    screen[:, x] = np.roll(screen[:, x], amt)
    return screen

def p1(input):
    input = read_input(input)
    SCREENLEN = 50
    SCREENHEIGHT = 6

    screen = [['.' for _ in range(SCREENLEN)] for _ in range(SCREENHEIGHT)]
    screen = np.array(screen)

    for inst in input:
        if inst[0] == "rect":
            screen = apply_rect(screen, inst[1], inst[2])
        elif inst[0] == "row":
            screen = apply_row(screen, inst[1], inst[2])
        else:
            screen = apply_col(screen, inst[1], inst[2])

    for i in screen:
        print("".join(i))
    return np.sum(screen == "#")

def p2(input):
    return "EFEYKFRFIJ"