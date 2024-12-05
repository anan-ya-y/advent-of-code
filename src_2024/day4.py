import utils

def transpose(input):
    transposed = []
    for c in range(len(input[0])):
        s = ""
        for r in range(len(input)):
            s += input[r][c]
        transposed.append(s)
    return transposed

def get_diags(input):
    diags = []
    ndiags = len(input) + len(input[0]) - 1
    for s in range(ndiags):
        diag = ""
        coords = [[r, s-r] for r in range(s+1)]
        for r, c in coords:
            if r < len(input) and c < len(input[0]):
                diag += input[r][c]

        diags.append(diag)

    return diags


def main(input):
    input = utils.split_and_strip(input)

    p1 = 0
    transposed = transpose(input)
    diags = get_diags(input)
    other_diags = get_diags(input[::-1])

    # rows
    p1 += sum([r.count("XMAS") + r.count("SAMX") for r in input])
    # cols
    p1 += sum([c.count("XMAS") + c.count("SAMX") for c in transposed])
    # diags
    p1 += sum([d.count("XMAS") + d.count("SAMX") for d in diags])
    # other diags
    p1 += sum([d.count("XMAS") + d.count("SAMX") for d in other_diags])


    p2 = 0
    for row in range(1, len(input)-1):
        for col in range(1, len(input[row])-1):
            if input[row][col] != "A":
                continue
            # above/below
            if input[row-1][col-1] == input[row-1][col+1] and input[row-1][col-1] in "MS" and \
                input[row+1][col-1] == input[row+1][col+1] and input[row+1][col-1] in "MS":
                p2 += (input[row-1][col-1] != input[row+1][col-1])

            # left/right
            if input[row-1][col-1] == input[row+1][col-1] and input[row-1][col-1] in "MS" and \
                input[row-1][col+1] == input[row+1][col+1] and input[row-1][col+1] in "MS":
                p2 += (input[row-1][col-1] != input[row-1][col+1])
                
    return p1, p2