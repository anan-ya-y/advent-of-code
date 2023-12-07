import utils

def p2(input):
    lines = input

    elves = lines.split("\n\n")
    elves = [e.strip().split('\n') for e in elves]
    elves = [[int(k) for k in e] for e in elves]
    elves = [sum(e) for e in elves]

    top = max(elves)
    elves.remove(top)
    t1 = max(elves)
    elves.remove(t1)
    t2 = max(elves)
    return (top + t1 + t2)

def p1(input):
    lines = input

    elves = lines.split("\n\n")
    elves = [e.strip().split('\n') for e in elves]
    elves = [[int(k) for k in e] for e in elves]
    elves = [sum(e) for e in elves]

    return max(elves)

