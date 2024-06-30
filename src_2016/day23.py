from .day12 import run_one_cmd
import re, utils

def run_inst_with_toggle(regs, input):    
    i = 0
    while i < len(input):
        # print(input)
        inst = input[i]
        if i == 4:
            regs["a"] += (regs["b"] * regs["d"])
            regs["c"] = 0
            regs["d"] = 0
            i = 9
            continue
        if "tgl" not in inst:
            regs, inc = run_one_cmd(regs, utils.split_and_strip(inst, " "))
            i += inc
            continue
        # Toggle
        reg_to_toggle = inst.split(" ")[1]
        toggleval = regs[reg_to_toggle]
        new_togglereg = i + toggleval
        i += 1
        if toggleval == 0:
            continue # do nothing 
        if new_togglereg >= len(input):
            continue # do nothing

        toggleline = input[new_togglereg].split(" ")
        if len(toggleline) == 2:
            # inc becomes dec, all others become inc
            this_inst = toggleline[0]
            if this_inst == "inc":
                input[new_togglereg] = " ".join(["dec"] + toggleline[1:])
            else:
                input[new_togglereg] = " ".join(["inc"] + toggleline[1:])

        elif len(toggleline) == 3:
            # jnz becomes cpy, all others become jnz
            this_inst = toggleline[0]
            if this_inst == "jnz":
                input[new_togglereg] = " ".join(["cpy"] + toggleline[1:])
            else:
                input[new_togglereg] = " ".join(["jnz"] + toggleline[1:])

    return regs

def p1(input):
    input = utils.split_and_strip(input)
    # I am SO GLAD that I setup day12 to take in strings. 
    regs = {"a": 7, "b": 0, "c": 0, "d": 0}
    regs = run_inst_with_toggle(regs, input)        
    return regs["a"]

def p2(input):
    input = utils.split_and_strip(input)
    regs = {"a": 12, "b": 0, "c": 0, "d": 0}
    regs = run_inst_with_toggle(regs, input)        
    return regs["a"]



