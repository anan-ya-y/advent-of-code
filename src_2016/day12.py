import re, utils

commands = []

def run_cmds(start_regs):
    regs = start_regs
    i = 0
    split_cmds = [utils.split_and_strip(c, " ") for c in commands]
    while i < len(commands):
        c = split_cmds[i]
        cmd, args = c[0], c[1:]
        if cmd == "jnz":
            x, y = args
            if x.isalpha():
                x = regs[x]
            
            if x != 0:
                i += int(y)
            else:
                i += 1

        if cmd == "inc":
            regs[args[0]] += 1
            i += 1
        if cmd == "dec":
            regs[args[0]] -= 1
            i += 1
        if cmd == "cpy":
            x, y = args
            if x.isalpha():
                x = regs[x]
              
            regs[y] = int(x)
            i += 1
    return regs
            
        

def p1(input):
    global commands
    commands = utils.split_and_strip(input)
    regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = run_cmds(regs)
    return regs["a"]

def p2(input):
    regs = {"a": 0, "b": 0, "c": 1, "d": 0}
    regs = run_cmds(regs)
    return regs["a"]