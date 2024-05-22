import utils

def p1(input):
    input = int(input)

    presents_per_elf = 10
    house_num = int(input * 0.02312)
    while True:
        if presents_per_elf * utils.sum_of_divisors(house_num) >= input:
            return house_num
        house_num += 1

def p2(input):
    input = int(input)

    presents_per_elf = 11
    max_houses_per_elf = 50

    house_num = int(input * 0.02)
    nchekced=0
    while True:
        nchekced += 1
        visiting_elves = [x for x in utils.get_divisors(house_num) if house_num//x < max_houses_per_elf]
        if sum(visiting_elves) * presents_per_elf >= input:
            print(nchekced)
            return house_num
        house_num += 1
