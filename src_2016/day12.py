import re, utils

all_commands = []

def run_cmds(start_regs, cmds=None):
    if cmds is None:
        commands = all_commands
    else:
        commands = cmds
    regs = start_regs
    i = 0
    split_cmds = [utils.split_and_strip(c, " ") for c in commands]
    while i < len(commands):
        c = split_cmds[i]
        regs, inc = run_one_cmd(regs, c)
        i += inc
    return regs

def run_one_cmd(regs, c):        
    cmd, args = c[0], c[1:]
    if cmd == "jnz":
        x, y = args
        if x.isalpha():
            x = regs[x]
        if y.isalpha():
            y = regs[y]
        y = int(y)
        x = int(x)

        if y == 0 or x == 0:
            i = 1
        elif x != 0:
            i = int(y)


    if cmd == "inc":
        regs[args[0]] += 1
        i = 1
    if cmd == "dec":
        regs[args[0]] -= 1
        i = 1
    if cmd == "cpy":
        x, y = args
        if x.isalpha():
            x = regs[x]
            
        regs[y] = int(x)
        i = 1
    return regs, i

            
        

def p1(input):
    global all_commands
    all_commands = utils.split_and_strip(input)
    regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = run_cmds(regs)
    return regs["a"]

def p2(input):
    regs = {"a": 0, "b": 0, "c": 1, "d": 0}
    regs = run_cmds(regs)
    return regs["a"]