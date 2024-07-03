def decompress(input, recursive=False): 
    if '(' not in input:
        # print("no parens", input)
        return input
    # print("in", input)

    output = ""
    i = 0
    while i < len(input):
        if input[i] == '(':
            endloc = (input[i:]).find(')')
            marker = input[i+1:i+endloc].split('x')
            length = int(marker[0])
            repeat = int(marker[1])

            start_repeat = i + endloc + 1
            end_repeat = start_repeat + length
            
            # for _ in range(repeat):
            if recursive:
                to_repeat = decompress(input[start_repeat:end_repeat], recursive=True)
            else:
                to_repeat = input[start_repeat:end_repeat]
            output += to_repeat * repeat

            i += endloc+1  + length

        else:
            output += input[i]
            i += 1
    return output

def p1(input):
    output = decompress(input)
    # remove whitespace 
    output = output.replace(" ", "").replace("\n", "")
    return len(output)

def p2(input):

    orig = input
    decompressed = decompress(input, recursive=True)
    # remove whitespace
    decompressed = decompressed.replace(" ", "").replace("\n", "")
    return len(decompressed)