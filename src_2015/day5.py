import utils

def is_nice(s, part):
    if part == 1:
        if "ab" in s or "cd" in s or "pq" in s or "xy" in s:
            return False
        
        nvowels = 0
        duplicate = False
        for i in range(len(s)):
            if nvowels >= 3 and duplicate:
                return True
            if s[i] in "aeiou":
                nvowels += 1
            if i < len(s) - 1:
                duplicate |= (s[i] == s[i+1])
        return nvowels >= 3 and duplicate
    else:
        pair = False
        repeat = False
        for i in range(len(s)):
            if pair and repeat:
                return True
            if i < len(s) - 1:
                pair |= (s[i:i+2] in s[i+2:])
            if i < len(s) - 2:
                repeat |= (s[i] == s[i+2])
        return pair and repeat

def p1(input):
    input = utils.split_and_strip(input)
    nice = 0
    for s in input:
        nice += is_nice(s, part=1)
    return nice

def p2(input):
    input = utils.split_and_strip(input)
    nice = 0
    for s in input:
        nice += is_nice(s, part=2)
    return nice
