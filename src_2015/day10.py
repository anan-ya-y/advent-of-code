def look_and_say(x):
    looksay = ""
    x = str(x)
    count = 0
    val = x[0]
    for c in x:
        if c == val:
            count += 1
        else:
            looksay += str(count) + val
            count = 1
            val = c

    looksay += str(count) + val
    return looksay

# def p1(input):
#     input = int(input)

#     for _ in range(40):
#         input = look_and_say(input)
#     return len(input)

# def p2(input):
#     input = int(input)

#     for _ in range(50):
#         input = look_and_say(input)
#     return len(input)

def main(input):
    input = int(input)
    for i in range(50):
        input = look_and_say(input)
        if i == 39:
            p1_ans = len(input)
    p2_ans = len(input)
    return p1_ans, p2_ans