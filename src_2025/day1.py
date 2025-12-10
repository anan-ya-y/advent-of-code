import utils

def main(input):
    input = utils.split_and_strip(input)

    p1 = 0
    p2 = 0

    prev_pos = 50
    pos = 50
    for line in input:
        dir = line[0]
        steps = int(line[1:])
        full_laps = steps // 100
        partials = steps % 100

        p2 += full_laps

        prev_pos = pos

        if dir == "R":
            pos += partials
        else:
            pos -= partials

        if (pos < 0 or pos > 100) and prev_pos != 0:
            p2 += 1

        pos %= 100
       
        if pos == 0:
            p1 += 1
            p2 += 1


    return p1, p2