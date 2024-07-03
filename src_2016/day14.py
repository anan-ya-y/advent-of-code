import utils
# SPEED DEPENDENT ON MD5 SPEED.

salt = ""
hashes = {}
def get_hash(h, n):
    if (h, n) in hashes:
        return hashes[(h, n)]
    original = h
    for _  in range(n):
        h = utils.md5(h)

    hashes[(original, n)] = h
    return h

def has_triple(hash):
    for i in range(2, len(hash)):
        if hash[i] == hash[i-1] and hash[i-1] == hash[i-2]:
            return hash[i]
    return -1

def is_valid(num, part=1):
    h = get_hash(salt+str(num), 1 if part == 1 else 2017)
    t = has_triple(h)
    if t == -1:
        return False
    for i in range(1, 1001):
        key = get_hash(salt+str(num+i), 1 if part == 1 else 2017)
        if t*5 in key:
            return True
    return False


def p1(input):
    global salt
    salt = input

    nkeys = 0
    i = 0
    while True:
        if is_valid(i):
            nkeys += 1
        if nkeys == 64:
            return i
        i += 1

def p2(input):
    global salt
    salt = input

    nkeys = 0
    i = 0
    while True:
        if is_valid(i, part=2):
            nkeys += 1
        if nkeys == 64:
            return i
        i += 1
