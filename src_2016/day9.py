def get_decompress_length(current_length, q, recurse=False):
    if q == []:
        return current_length, []
    
    # pull the next item off the stack:
    qty, item = q.pop(0)    
    if "(" not in item and ")" not in item:
        return current_length + (qty * len(item)), q
    
    new_length = 0
    i = 0
    while i < len(item):
        if item[i] == "(":
            end_index = item[i:].index(")")
            multiply_str = item[i+1:i+end_index] # "4x2"
            vals = list(map(int, multiply_str.split("x")))
            next_chars = item[i+end_index+1:i+end_index+vals[0]+1]
            if recurse:
                q.append((vals[1]*qty, next_chars))
            else:
                new_length += vals[0]*vals[1]
            i += vals[0]+end_index+1
        else:
            i += 1
            new_length += 1

    return current_length + (new_length * qty), q

def p1(input):
    input = input.replace(" ", "").replace("\n", "")
    length, _ = get_decompress_length(0, [(1, input)], recurse=False)
    return length

def p2(input):
    input = input.replace(" ", "").replace("\n", "")
    length = 0
    queue = [(1, input)]
    while queue != []:
        length, queue = get_decompress_length(length, queue, recurse=True)

    return length
