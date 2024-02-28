import utils
import re

def parse_input(lines):
    stackdrawing, moves_text = lines.split('\n\n')

    stacks = parse_stacks(stackdrawing.split('\n'))
    moves = parse_moves(moves_text.split('\n'))

    return stacks, moves

def parse_stacks(stackdrawing):
    nstacks = len(stackdrawing[-1].strip().split("   "))
    stacks = [[] for _ in range(nstacks)]

    for row in range(len(stackdrawing)-2, -1, -1):
        elements = list(stackdrawing[row])[1::4]
        for i in range(len(elements)):
            if elements[i] == ' ':
                continue
            stacks[i].append(elements[i])

    return stacks


def parse_moves(lines):
    moves = []
    for line in lines:
        if line == '':
            continue
        n, from_stack, to_stack = re.findall(r'move (\d+) from (\d+) to (\d+)',
                                                 line)[0]
        moves.append((int(n), int(from_stack), int(to_stack)))
    return moves

def p1(input):
    lines = input
    stacks, moves = parse_input(lines)

    for move in moves:
        n, from_stack, to_stack = move
        for _ in range(n):
            stacks[to_stack-1] += stacks[from_stack-1].pop()

    stack_endpts = []
    for s in stacks:
        stack_endpts.append(s[-1])

    return ("".join(stack_endpts))

def p2(input):
    lines = input
    stacks, moves = parse_input(lines)

    for move in moves:
        n, from_stack, to_stack = move
        removed = stacks[from_stack-1][-n:]
        stacks[from_stack-1] = stacks[from_stack-1][:-n]
        stacks[to_stack-1] += removed

    stack_endpts = []
    for s in stacks:
        stack_endpts.append(s[-1])

    return ("".join(stack_endpts))

    
# p1("inputs/5.real.txt")
# p2("inputs/5.real.txt")