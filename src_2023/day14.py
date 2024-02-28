import utils

def move_rocks_horizontal(row, dir):
    r = row.split("#")
    # replace with Os first, then dots
    new = []
    for st in r:
        nOs = st.count("O")
        nDots = st.count(".")
        if dir == "west":
            new.append("O"*nOs + "."*nDots)
        elif dir == "east":
            new.append("."*nDots + "O"*nOs)

    return "#".join(new)

def get_load(input):
    sum = 0
    for i in range(len(input)):
        row = input[i]
        weight = len(row) - i
        sum += (row.count("O") * weight)
    return sum

def tilt_EW(trans, dir):
    new_trans = []
    for row in trans:
        new_row = move_rocks_horizontal(row, dir)
        new_trans.append(new_row)
    return new_trans

def tilt_NS(input, dir):
    x = utils.transpose_string_matrix(input)
    if dir == "north":
        x = tilt_EW(x, "west")
    elif dir == "south":
        x = tilt_EW(x, "east")
    return utils.transpose_string_matrix(x)

def p1(input):
    input = utils.split_and_strip(input)
    x = tilt_NS(input, "north")
    load = get_load(x)
    return load

def p2(input):
    input = utils.split_and_strip(input)
    x = input
    load = 0

    ncycles = 1000000000
    asymptote = {}
    for i in range(ncycles):
        x = tilt_NS(x, "north")
        x = tilt_EW(x, "west")
        x = tilt_NS(x, "south")
        x= tilt_EW(x, "east")

        # If we're in some sort of asymptotic state, just
        # math thru the rest of the iterations
        if "\n".join(x) in asymptote:
            asymptote_at = asymptote["\n".join(x)]
            cycle_length = i - asymptote_at 
            print("Asymptote at", asymptote_at, "with cycle length", cycle_length)
            diff = ((ncycles - i ) % cycle_length) - 1 # Because we're 0-indexed
            print ("should look for #", diff + asymptote_at)
            for mat in asymptote:
                iter = asymptote[mat]
                if iter == (diff + asymptote_at):
                    return get_load(mat.split("\n"))
            break
        else:
            asymptote["\n".join(x)] = i

    return get_load(x)