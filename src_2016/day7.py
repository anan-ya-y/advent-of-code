import re, utils

def is_abba(s):
    if len(s) != 4:
        return False
    return s[:2] == s[2:][::-1] and s[0] != s[1]

def has_abba(s):
    for i in range(len(s) - 3):
        if is_abba(s[i:i+4]):
            return True
    return False

def p1(input):
    input = utils.split_and_strip(input)
    ans = 0
    for line in input:
        all_splits = set(re.split(r'\[|\]', line))
        square_brackets = set(utils.get_all_chars_in_squarebrackets(line))
        non_square_brackets = all_splits.difference(square_brackets)
        num_in_square = sum([has_abba(s) for s in square_brackets])
        num_out_square = sum([has_abba(s) for s in non_square_brackets])
        valid = (num_in_square == 0) and (num_out_square > 0)        
        ans += valid
    return ans

def is_aba(s):
    return s == s[::-1] and len(s) == 3 and s[0] != s[1]

def get_abas(s):
    abas = []
    for i in range(len(s) - 2):
        if is_aba(s[i:i+3]):
            abas.append(s[i:i+3])
    return abas

def get_bab(aba):
    return aba[1] + aba[0] + aba[1]

def p2(input):
    input = utils.split_and_strip(input)
    ans = 0
    for line in input:
        all_splits = set(re.split(r'\[|\]', line))
        square_brackets = set(utils.get_all_chars_in_squarebrackets(line))
        non_square_brackets = all_splits.difference(square_brackets)
        square_brackets = " ".join(square_brackets)
        non_square_brackets = " ".join(non_square_brackets)

        abas = get_abas(non_square_brackets)
        for aba in abas:
            bab = get_bab(aba)
            if bab in square_brackets:
                ans += 1
                break
    return ans