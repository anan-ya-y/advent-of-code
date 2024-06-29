import re, utils
from random import shuffle

def perform(cmd, s):
    if cmd.startswith("swap position"):
        k = re.search(r"swap position (\d+) with position (\d+)", cmd)
        k = list(map(int, k.groups()))
        s[k[0]], s[k[1]] = s[k[1]], s[k[0]]
    if cmd.startswith("swap letter"):
        k = re.search(r"swap letter (\w) with letter (\w)", cmd)
        k = k.groups()
        i1 = s.index(k[0])
        i2 = s.index(k[1])
        s[i1], s[i2] = s[i2], s[i1]
    if re.search(r"rotate (left|right)", cmd):
        cmd += "s"
        k = re.search(r"rotate ([a-z]+) (\d+) steps", cmd)
        k = k.groups()
        val = int(k[1]) % len(s)
        if k[0] == "left":
            s = s[val:] + s[:val]
        else:
            s = s[-val:] + s[:-val]
    if cmd.startswith("rotate based"):
        k = re.search(r"rotate based on position of letter (\w)", cmd)
        k = k.groups()[0]
        i = s.index(k)
        i += (2 if i >= 4 else 1)
        s = perform(f"rotate right {i} steps", s)
    if cmd.startswith("reverse positions"):
        k = re.search(r"reverse positions (\d+) through (\d+)", cmd)
        k = list(map(int, k.groups()))
        s = s[:k[0]] + s[k[0]:k[1]+1][::-1] + s[k[1]+1:]
    if cmd.startswith("move position"):
        k = re.search(r"move position (\d+) to position (\d+)", cmd)
        k = list(map(int, k.groups()))
        letter = s[k[0]]
        removed = s[:k[0]] + s[k[0]+1:]
        s = removed[:k[1]] + [letter] + removed[k[1]:]
    return s

def scramble(cmds, s):
    if type(s) == str:
        s = list(s)
    for line in cmds:
        s = perform(line, s)
    return "".join(s)

def p1(input):
    input = utils.split_and_strip(input)
    s = "abcdefgh"
    return scramble(input, s)

# haha, randomized algo style!!
def p2(input):
    target = "fbgdceah"
    input = utils.split_and_strip(input)

    seen_perms = set()
    while True:
        s = list(target)
        shuffle(s)
        str_shuffle = "".join(s)
        if str_shuffle in seen_perms:
            continue
        seen_perms.add(str_shuffle)
        scrambled = scramble(input, s)
        # print(str_shuffle, scrambled)
        if scrambled == target:
            return str_shuffle