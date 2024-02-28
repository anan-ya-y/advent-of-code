import utils

def HASH(x):
    val = 0
    for l in x:
        if l == "\n":
            continue

        val += ord(l)
        val *= 17
        val %= 256
    return val

def HASHMAP(boxes, values, inst):
    if "-" in inst:
        label = inst[:-1]
        boxnum = HASH(label)
        if label in boxes[boxnum]:
            boxes[boxnum].remove(label)
            values[(boxnum, label)] = -1
    elif "=" in inst:
        label, focal_length = inst.split("=")
        boxnum = HASH(label)
        focal_length = int(focal_length)
        if label in boxes[boxnum]:
            values[(boxnum, label)] = focal_length
        else:
            boxes[boxnum].append(label)
            values[(boxnum, label)] = focal_length
    return boxes, values

def get_scores(boxes, values):
    total = 0

    for b in range(len(boxes)):
        box = boxes[b]
        for v in range(len(box)):
            boxnum = b
            slotnum = v
            focal_length = values[(boxnum, box[v])]
            if focal_length != -1:
                total += (boxnum+1) * (slotnum+1) * focal_length

    return total

def p1(input):
    vals = input.split(",")

    sum = 0
    for v in vals:
        sum += HASH(v)
    return sum

def p2(input):
    instructions = input.split(",")

    boxes = [ [] for i in range(256) ] 
        # Can't write [[]]*256 because it's a shallow copy
    values = {}
    for inst in instructions:
        boxes, values = HASHMAP(boxes, values, inst)
    
    return get_scores(boxes, values)
