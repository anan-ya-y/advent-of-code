import re, utils

AND = "AND"
OR = "OR"
LSHIFT = "LSHIFT"
RSHIFT = "RSHIFT"
NOT = "NOT"

# Note: Not(a) = a XOR 1.  
NOT_CONST = (1<<16)-1 #(2^16)-1 = 15 1s. 
    
operations = {
    AND: lambda a, b: a & b, 
    OR: lambda a, b: a | b, 
    LSHIFT: lambda a, b: a << int(b),
    RSHIFT: lambda a, b: a >> int(b),
    NOT: lambda a, b: b ^ NOT_CONST
}


def split_by_op(inst):
    k = re.split(rf"({AND}|{OR}|{LSHIFT}|{RSHIFT}|{NOT})", inst)
    k = [x.strip() for x in k]
    if len(k) == 3:
        return k[1], [k[0], k[2]]
    return "ASSIGN", k[0]

def perform_op(reg_vals, inst):
    # print(inst)
    i, target = inst
    target = target.strip()
    inst_type, nums = split_by_op(i)
    try:
        if inst_type == "ASSIGN":
            if nums.isdigit():
                reg_vals[target] = int(nums)
            else:
                reg_vals[target] = reg_vals[nums]
        else:
            if not nums[0].isdigit():
                nums[0] = reg_vals[nums[0]]
            if not nums[1].isdigit():
                nums[1] = reg_vals[nums[1]]
            nums = [int(x) for x in nums]
            reg_vals[target] = operations[inst_type](nums[0], nums[1])
        return True, reg_vals
    except Exception as e:
        return False, reg_vals
    
def get_dependents(operations):
    i, target = operations
    inst_type, nums = split_by_op(i)
    ans = []
    if inst_type == "ASSIGN":
        if not nums.isdigit():
            ans.append(nums)
    else:
        for n in nums:# only 2 but whatebz
            if not n.isdigit() and n != '':
                ans.append(n)

    return ans

def parse_input(input):
    operations = []
    for line in utils.split_and_strip(input):
            operations.append(line.split(" -> "))
    return operations

def get_wire_a(parsed_input, default_dict = {}):
    k = [(a, b) for a, b in parsed_input if b == "a"][0]
    s = [k]
    reg_vals = default_dict
    reg_vals[''] = 0
    while s:
        item = s.pop()

        # if inst can be pefromed, perform it. 
        # else, add it and dependents to stack. 
        performed, reg_vals = perform_op(reg_vals, item)
        if not performed:
            s.append(item)
            for dep in get_dependents(item):
                if dep in reg_vals:
                    continue
                dep_inst = [x for x in parsed_input if x[1] == dep][0]
                s.append(dep_inst)
    return reg_vals["a"]

def p1(input):
    input = parse_input(input)
    return get_wire_a(input)

def p2(input):
    wire_a = p1(input)
    input = parse_input(input)
    default_dict = {'b': wire_a}
    return get_wire_a(input, default_dict)

