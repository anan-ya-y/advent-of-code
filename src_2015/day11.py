alphabet = "abcdefghijklmnopqrstuvwxyz"

def to_nums(word):
    return [alphabet.index(c) for c in word]
def to_letters(nums):
    return "".join(alphabet[n] for n in nums)

def increment_password(nums):    
    nums[-1] += 1
    if nums[-1] == 26:
        if len(nums) == 1:
            return [0, 0]
        nums[-1] = 0
        nums = increment_password(nums[:-1]) + [nums[-1]]

    return nums

def is_valid(pwd):
    # no i, o, l
    if any(c in pwd for c in "iol"):
        return False
    
    # increasing straight of 3 letters
    hasStraight = False
    for i in range(len(alphabet)-2):
        straight = alphabet[i:i+3]
        hasStraight |= straight in pwd
    if not hasStraight:
        return False
        
    # two different non-overlapping pairs of letters
    pairs = [c*2 for c in alphabet]
    pairs = [p for p in pairs if p in pwd]
    return len(pairs) >= 2

def get_next_valid(pwd):
    password = to_nums(pwd)
    password = increment_password(password)
    while not is_valid(to_letters(password)):
        password = increment_password(password)
    password = to_letters(password)
    return password

p1_ans = ""
p2_ans = ""
def run(input):
    global p1_ans, p2_ans
    p1_ans = get_next_valid(input)
    p2_ans = get_next_valid(p1_ans)

def p1(input):
    run(input)
    return p1_ans

def p2(input):
    return p2_ans