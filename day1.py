import utils

def p1(filename):
    lines = utils.get_file_content(filename)

    elves = lines.split("\n\n")
    elves = [e.split('\n') for e in elves]
    elves = [[int(k) for k in e] for e in elves]
    elves = [sum(e) for e in elves]

    top = max(elves)
    elves.remove(top)
    t1 = max(elves)
    elves.remove(t1)
    t2 = max(elves)
    print(top + t1 + t2)

p1('inputs/1.real.txt')

