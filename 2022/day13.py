import utils
import ast
#https://stackoverflow.com/questions/1894269/how-to-convert-string-representation-of-list-to-a-list

# s must INCLUDE open and close parens
def parse_string(s):
    return ast.literal_eval(s)

def parse_input(input, part=1):
    if part==2:
        signals = input.split("\n")
        arr = []
        for s in signals:
            if s != '':
                arr.append(parse_string(s))
        return arr

    signals = input.split("\n\n")
    arr = []
    for signal in signals:
        l, r = signal.strip().split("\n")
        arr.append((parse_string(l), parse_string(r)))

    return arr

# copied from day ?? of 2023:
# (returns in DECREASING) order??
def binary_sort(arr):
    if len(arr) == 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    bs_left = binary_sort(left)
    bs_right = binary_sort(right)

    arr = []
    # Merge the two arrays:
    while len(bs_left) > 0 and len(bs_right) > 0:
        if inRightOrder(bs_right[0], bs_left[0]) > 0: # right is better than left
            arr.append(bs_left.pop(0))
        else:
            arr.append(bs_right.pop(0))
    while len(bs_left) > 0:
        arr.append(bs_left.pop(0))
    while len(bs_right) > 0:
        arr.append(bs_right.pop(0))

    return arr

# 1 if l < r, 0 if l = r, -1 if l > r
def inRightOrder(l, r):
    # print(l, r)
    if type(l) == int and type(r) == int:
        # print(l, r, "int comparison")
        return 1 if l < r else (0 if l == r else -1)
    if type(l) == int and type(r) != int:
        return inRightOrder([l], r)
    if type(l) != int and type(r) == int:
        return inRightOrder(l, [r])
    for i in range(min(len(l), len(r))):
        el, ar = l[i], r[i]
        # print("for loop", el, ar)
        if type(el) == int and type(ar) == int and el != ar:
            # print("el, ar int comp")
            return 1 if el < ar else -1
        if type(el) != int or type(ar) != int:
            c = inRightOrder(el, ar)
            if c != 0:
                return c
    if len(l) != len(r):
        return 1 if len(l) < len(r) else -1
    return 0

def p1(input):
    signals = parse_input(input)
    sum = 0
    for i in range(1, 1+len(signals)):
        l, r = signals[i-1]
        if inRightOrder(l, r) >= 0:
            sum += i
    return sum

def p2(input):
    signals = parse_input(input, part=2)
    signals += [[[2]], [[6]]]

    sorted = binary_sort(signals)[::-1]

    return (1+sorted.index([[2]])) * (1+sorted.index([[6]]))