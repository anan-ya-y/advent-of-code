import hashlib

def p1(input):
    input = bytes(input, "utf-8")
    i = 1
    while True:
        h = hashlib.md5(input + str(i).encode() ).hexdigest()
        if h[:5] == "00000":
            return i
        i += 1
    return -1

def p2(input):
    input = bytes(input, "utf-8")
    i = 1
    while True:
        h = hashlib.md5(input + str(i).encode() ).hexdigest()
        if h[:6] == "000000":
            return i
        i += 1