
def p1(input): # just gonna do this manually. 
    n = int(input)
    elves = [i for i in range(1, n+1)]

    while len(elves) > 1:
        new_elves = elves[::2]
        if len(elves) % 2 == 1:
            elves = [new_elves[-1]] + new_elves[:-1]
        else:
            elves = new_elves
 

    return elves[0]

def p2_s(n):
    elves = [i for i in range(1, n+1)]
    while len(elves) > 1:
        half_idx = len(elves) // 2
        elves.remove(elves[half_idx])
        elves = elves[1:] + [elves[0]]
    return elves[0]

def p2(input):
    n = int(input)
    import math

    return n - math.pow(3, int(math.log(n, 3)))

    # found the pattern :)
    for i in range(1, 100):
        print(f"{i}, {p2_s(i)}")

    return 3

