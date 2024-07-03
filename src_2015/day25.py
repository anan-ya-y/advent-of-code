import utils

def get_next_num(i):
    return (i * 252533) % 33554393
def get_next_pos(r, c):
    if r == 1:
        return c+1, 1
    return r-1, c+1

def p1(input):
    desired = (2978, 3083) # from input
    position = (1, 1)
    val = 20151125

    while position != desired:
        position = get_next_pos(*position)
        val = get_next_num(val)

    return val