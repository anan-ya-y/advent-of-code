import re, utils

def get_correct_checksum(name):
    freqs = utils.get_n_most_frequent(name, 5)
    freqs = sorted(freqs, key=lambda x: 10000*x[1] - ord(x[0]), reverse=True)
    return "".join([x[0] for x in freqs])[:5]

def get_checksum_name_sectorid(line):
    checksum = re.split(r'\[|\]', line)[1]
    name = line[:-10]
    sector_id = line[-10:-7]
    return checksum, name, int(sector_id)

def get_score(line):
    checksum, name, sector_id = get_checksum_name_sectorid(line)
    name = name.replace("-", "")

    if get_correct_checksum(name) != checksum:
        return 0
    
    return int(sector_id)

def shift_letter(letter, shift):
    letternum = ord(letter) - 97
    new_letternum = (letternum + shift) % 26
    return chr(new_letternum + 97)

def shift_name(name, shift):
    return "".join([shift_letter(x, shift) if x != "-" else "-" for x in name])

def p1(input):
    input = utils.split_and_strip(input)
    ans = 0
    for line in input:
        ans += get_score(line)
    return ans

def p2(input):
    input = utils.split_and_strip(input)

    for line in input:
        if get_score(line) == 0:
            continue
        checksum, name, sector_id = get_checksum_name_sectorid(line)
        name = shift_name(name, sector_id)
        if "north" in name:
            return sector_id
