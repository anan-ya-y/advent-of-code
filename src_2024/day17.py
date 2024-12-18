import re, utils

def parse_input(inp):
    i1, i2 = utils.split_and_strip(inp, "\n\n")
    i1 = i1.split("\n")
    registers = {"A": 0, "B": 0, "C": 0}
    for r in i1:
        ans = re.findall(r"Register (\w): (\d+)", r)
        registers[ans[0][0]] = int(ans[0][1])

    instructions = list(map(int, i2.split(": ")[1].split(",")))
    return registers, instructions

def xor(a, b):
    return int((a & ~b) | (~a & b))

# returns registers, pointer, output
def one_step(registers, instructions, pointer):
    opcode = instructions[pointer]
    operand = instructions[pointer+1]

    if operand != 7:
        combo_operand = operand if operand <= 3 else registers[chr(operand+64-3)]
    else:
        combo_operand = None
    literal_operand = operand
    pointer += 2
    output = None

    if opcode in [0, 6, 7]:
        numerator = registers["A"]
        denominator = 2 ** combo_operand
        if opcode == 0:
            target_register = "A"
        elif opcode == 6:
            target_register = "B"
        else:
            target_register = "C"
        registers[target_register] = numerator // denominator

    if opcode == 1:
        registers["B"] = xor(registers["B"], literal_operand)
    
    if opcode == 2:
        registers["B"] = combo_operand % 8 # keep lowest 3 bits?
    
    if opcode == 3:
        if registers["A"] != 0:
            pointer = literal_operand
    
    if opcode == 4:
        registers["B"] = xor(registers["B"], registers["C"])
    
    if opcode == 5:
        output = combo_operand % 8

    return registers, pointer, output

def run_program(registers, instructions):
    pointer = 0
    outputs = []

    while pointer < len(instructions):
        registers, pointer, out = one_step(registers, instructions, pointer)
        if out is not None:
            outputs.append(out)

    return outputs

# returns True if a is before b, False if a is after b
# returns True if a == b
def before(a, b):
    if len(a) < len(b):
        return True
    if len(a) > len(b):
        return False
    # lengths are equal. 
    for i in range(len(a)-1, -1, -1):
        if a[i] < b[i]:
            return True
        if a[i] > b[i]:
            return False
    return True

def main(inp):
    registers, instructions = parse_input(inp)
    p2_target =  instructions
    instructions_str = "".join(map(str, p2_target))
    p1 = run_program(registers.copy(), instructions) 
    sample = False

    if sample:
        ans = int(instructions_str[::-1], 8) * 8
        registers["A"] = ans
        print(ans)
    else:
        # THANK YOU REDDIT (-ish. only that we should skip by powers of 2.)
        registers["A"] = (1 << (3 * (len(p2_target)-1)))# smallest possible value

    done = False
    while not done:
        output = run_program(registers.copy(), instructions)
        print(output, utils.to_base_n(registers["A"], 8), p2_target)
        if output == p2_target:
            done = True
            continue
        ra_val = registers["A"]

        # check if the current position is correct
        farthest_wrong = len(p2_target) - 1
        while farthest_wrong >= 0:
            if output[farthest_wrong] != p2_target[farthest_wrong]:
                break
            farthest_wrong -= 1

        # biggest digit controls element -1
        # smallest digit controls element 0.
        if not sample:
            registers["A"] += (1 << 3*(farthest_wrong))
        else:
            registers["A"] += 1    

    while run_program(registers.copy(), instructions) == instructions:
        registers["A"] -= 1
        
    return ",".join(map(str, p1)), registers["A"]+1


