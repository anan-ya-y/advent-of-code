import utils
C = complex

dirs = {
    "R": C(0, 1),
    "L": C(0, -1),
    "U": C(-1, 0),
    "D": C(1, 0)
}

# Pick's: A = interior + b/2 - 1
# https://artofproblemsolving.com/wiki/index.php?title=Shoelace_Theorem

def get_border_and_corners(input):
    position = C(0, 0)
    nborder = 0
    corners = []
    for order in input:
        dir, amt, _ = order.split(" ")
        corners.append(position)
        position += dirs[dir] * int(amt)
        nborder += int(amt)
    return nborder, corners

def print_grid(grid):
    ncols = max([int(c.imag) for c in grid]) + 1
    nrows = max([int(c.real) for c in grid]) + 1

    for i in range(nrows):
        for j in range(ncols):
            if C(i, j) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()

def p1(input):
    input = utils.split_and_strip(input)
    border, corners = get_border_and_corners(input)

    corners = [(int(c.real), int(c.imag)) for c in corners]

    s = 0
    for i in range(len(corners)):
        x1, y1 = corners[i]
        x2, y2 = corners[(i+1)%len(corners)]
        s += (x1*y2 - x2*y1)
    interior = abs(s)/2

    return int(interior + border/2 + 1)
    


def p2(input):
    input = utils.split_and_strip(input)

    new_input = []
    for line in input:
        hex = line.split(" ")[-1]
        amount = int(hex[2:-2], 16)
        dir = ""
        if hex[-2] == "0":
            dir = "R"
        elif hex[-2] == "1":
            dir = "D"
        elif hex[-2] == "2":
            dir = "L"
        elif hex[-2] == "3":
            dir = "U"
        
        new_input.append(dir + " " + str(amount) + " asdf")

    return p1("\n".join(new_input))