import re, utils
import operator

commands = []

reg_cmds = {
    "hlf": lambda x: x//2,
    "tpl": lambda x: x*3,
    "inc": lambda x: x+1
}
# returns amount to jump by
inst_cmds = {
    "jmp": lambda val: val,
    "jie": lambda reg, val: val if reg % 2 == 0 else 1,
    "jio": lambda reg, val: val if reg == 1 else 1
}

def process_input(input):
    commands = []
    input = utils.split_and_strip(input)
    for line in input:
        line = re.split(r'[ ,]+', line)
        if len(line) == 3:
            line[2] = int(line[2])
        commands.append((line[0], line[1:]))
    return commands

def run_cmds(start_regs):
    regs = start_regs
    i = 0
    while i < len(commands):
        cmd, args = commands[i]
        reg = args[0]
        if cmd in reg_cmds:
            regs[reg] = reg_cmds[cmd](regs[reg])
            i += 1
        elif cmd in inst_cmds:
            if cmd == "jmp":
                i += inst_cmds[cmd](int(reg))
            else:
                i += inst_cmds[cmd](regs[reg], int(args[1]))
    return regs

def p1(input):
    global commands
    commands = process_input(input)

    regs = {"a": 0, "b": 0}
    regs = run_cmds(regs)
    print(regs)
    return regs["b"]
        

def p2(input):
    regs = {"a": 1, "b": 0}
    regs = run_cmds(regs)
    return regs["b"]