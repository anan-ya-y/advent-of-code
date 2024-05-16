def p1(input):
    return input.count('(') - input.count(')')

def p2(input):
    floor = 0
    for i in range(len(input)):
        floor += 1 if input[i] == '(' else -1
        if floor == -1:
            return i+1