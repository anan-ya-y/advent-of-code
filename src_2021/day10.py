import utils
POINTS = {
    ")": 3, 
    "]": 57, 
    "}": 1197, 
    ">": 25137, 
    None: 0
}

POINTS_FIX = {
    ")": 1, 
    "]": 2, 
    "}": 3, 
    ">": 4
}

PAIR = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

def check_line(line):
    stack = []
    for c in line:
        if c in PAIR:
            stack.append(c)
        else:
            if not stack or c != PAIR[stack.pop()]:
                return POINTS[c]
    return stack

def main(input):
    input = utils.split_and_strip(input)

    p1 = 0
    p2scores = []
    for line in input:
        p = check_line(line)
        if type(p) == int:
            p1 += p
        else: # part 2: fix line. p is the stack
            answers = [PAIR[k] for k in p][::-1]
            score = 0
            for a in answers:
                score *= 5
                score += POINTS_FIX[a]
            p2scores.append(score)
    p2scores.sort()
    return p1, p2scores[len(p2scores)//2]