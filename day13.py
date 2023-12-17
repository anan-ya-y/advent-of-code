import utils

def reflect(input, line_num):
    nrows_to_check = min(line_num, len(input)-line_num)
    after = input[line_num:min(len(input), line_num+nrows_to_check)]
    before = input[line_num-nrows_to_check:line_num]

    return after[::-1] == before and before != []

def reflect_smudge(input, line_num):
    nrows_to_check = min(line_num, len(input)-line_num)
    after = input[line_num:min(len(input), line_num+nrows_to_check)]
    before = input[line_num-nrows_to_check:line_num]

    ndiffs = 0
    for a, b in zip(after[::-1], before):
        for i in range(len(a)):
            if a[i] != b[i]:
                ndiffs += 1
            if ndiffs > 1:
                return False
    return ndiffs == 1


def transpose(input):
    ans = []
    for col in range(len(input[0])):
        s = ""
        for r in range(len(input)):
            s += input[r][col]
        ans.append(s)

    return ans

def p1(input):
    input = input.split("\n\n")
    s = 0
    for i in input:
        inp = utils.split_and_strip(i)
        found = False
        for j in range(len(inp), 0, -1):
            if found:
                break
            if reflect(inp, j):
                # print(j, "horizontal")
                s += (100*j)
                found = True
        transinp = transpose(inp)
        for j in range(len(transinp), 0, -1):
            if found:
                break
            if reflect(transinp, j):
                # print(j, "vertical")
                s += j
                found = True
    return s

def p2(input):
    input = input.split("\n\n")
    
    s = 0
    for i in input:
        inp = utils.split_and_strip(i)
        found = False
        for j in range(len(inp), 0, -1):
            if found:
                break
            if reflect_smudge(inp, j):
                # print(j, "horizontal")
                s += (100*j)
                found = True
        transinp = transpose(inp)
        for j in range(len(transinp), 0, -1):
            if found:
                break
            if reflect_smudge(transinp, j):
                # print(j, "vertical")
                s += j
                found = True
    return s