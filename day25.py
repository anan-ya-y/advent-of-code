import utils
import math

snafu_digits = {
    '1': 1, 
    '2': 2, 
    '0': 0, 
    '-': -1, 
    '=': -2
}

def dec_to_base5(num):
    n = 0
    ndigits = int(math.log(num, 5)) + 1
    for i in range(ndigits-1, -1, -1):
        n *= 10
        n += (num // (5 **i))
        num %= (5**i)

    return n

def snafu_to_dec(num):
    n = 0
    for d in num:
        n *= 5
        n += snafu_digits[d]
    return n

def base5_to_snafu(num):
    n = ""
    carryover = 0
    while num > 0:
        d = num % 10
        d += carryover
        if d == 0 or d == 1 or d == 2:
            n = str(d) + n
        if d == 3:
            n = "=" + n
        if d == 4:
            n = "-" + n
        if d == 5:
            n = "0" + n
        carryover = 0 if d < 3 else 1

        num //= 10
    if carryover == 1:
        n = "1" + n

    return n

def dec_to_snafu(num):
    x = dec_to_base5(num)
    return base5_to_snafu(x)

def p1(filename):
    lines = utils.get_file_stripped_lines(filename)
    dec_sum = 0
    for l in lines:
        dec_sum += snafu_to_dec(l)

    print(dec_to_snafu(dec_sum))
    


p1("inputs/25.real.txt")