import utils

def get_priority(c):
    o = ord(c)
    if o > 95:
        o -= 96
    else:
        o = (o-65) + 27
    return o


def p1(input):
    lines = utils.split_and_strip(input)

    sum = 0
    for line in lines:
        c1 = line[:len(line)//2]
        c2 = line[len(line)//2:]
        s1 = set(c1)
        s2 = set(c2)
        doublepacked = s1.intersection(s2)

        o = get_priority(list(doublepacked)[0])

        sum += o
    return (sum)

def p2(input):
    lines = utils.split_and_strip(input)

    sum = 0
    for i in range(0, len(lines), 3):
        c1 = lines[i]
        c2 = lines[i+1]
        c3 = lines[i+2]
        
        common = set(c1).intersection(set(c2))
        common = common.intersection(set(c3))

        o = get_priority(list(common)[0])
        sum += o

    return (sum)

# p1("inputs/3.real.txt")
# p2("inputs/3.real.txt")