import utils

def p1(input):
    lines = utils.split_and_strip(input)

    cycles = [1]
    x = 1
    for line in lines:
        if line == "noop":
            cycles.append(x)
        else:
            cycles.append(x)
            x += int(line.split(" ")[-1])
            cycles.append(x)
            
    interesting = 0
    for i in [20, 60, 100, 140, 180, 220]:
        interesting += cycles[i-1] * i
    return interesting

def p2(input):
    lines = utils.split_and_strip(input)

    cycles = [1]
    x = 1
    for line in lines:
        if line == "noop":
            cycles.append(x)
        else:
            cycles.append(x)
            x += int(line.split(" ")[-1])
            cycles.append(x)
            

    rows = ""
    for i in range(len(cycles)-1):
        c = cycles[i]
        
        current_position = i % 40
        if abs(c-current_position) <= 1:
            rows += "#"
        else:
            rows += "."
    
    for i in range(6):
        print(rows[40*i:40*(i+1)])

    return "RZHFGJCB"