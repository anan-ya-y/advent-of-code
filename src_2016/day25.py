from .day12 import run_one_cmd 
import utils
# yay, no toggles. 

def run_inst_with_out(regs, cmds):
    i = 0
    while i < len(cmds):
        inst = cmds[i]
        if "out" in inst:
            out = inst.split(" ")[1]
            yield regs[out]
            i += 1
            continue
        c = inst.split(" ")
        regs, inc = run_one_cmd(regs, c)
        i += inc
    # return regs

def p1(input):
    # couldve brute forced it if it weren't for that bug! 
    cmds = utils.split_and_strip(input)
    
    start_val = 0

    while True:
        outs = []
        regs = {"a": start_val, "b": 0, "c": 0, "d": 0}
        for o in run_inst_with_out(regs, cmds):
            outs.append(o)
            if len(outs) > 1 and outs[-2] == outs[-1] or len(outs) > 13:
                break

        # print(start_val, outs)
        if all([outs[i] == i % 2 for i in range(len(outs))]):
            return start_val
        start_val += 1

    return -1

def p2(input):
    return 25

def run_forreals(a):
    d = a + (14*182)
    a = d
    while a > 0:
        c = 2 - (a%2)
        a //= 2
        b = 2-c
        print(b)
