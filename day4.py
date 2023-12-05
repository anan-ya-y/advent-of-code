import re, utils

def read_card(line):
    id = re.findall(r"Card * (\d+):", line)[0]
    winning_nums, our_nums = line.split(":")[1].split("|")
    winning_nums = re.findall(r"(\d+)", winning_nums)
    our_nums = re.findall(r"(\d+)", our_nums)
    
    return int(id), map(int, winning_nums), map(int, our_nums)

def p1(filename):
    lines = utils.read_file(filename)
    cards = [read_card(l) for l in lines]
    sum = 0
    for id, winning_nums, ours in cards:
        winning = set(winning_nums).intersection(set(ours))
        nwinning = len(winning)
        if nwinning > 0:
            sum += (2 ** (nwinning - 1))

    print(sum)

def p2_alternate(filename):
    lines = utils.read_file(filename)
    cards = [read_card(l) for l in lines]
    card_dict = {id: len(set(w).intersection(set(o))) for (id, w, o) in cards}
    card_stack = [i for i in range(1, len(cards) + 1)]
    ncards = 0
    while len(card_stack) > 0:
        id = card_stack.pop(0)
        ncards += 1

        if card_dict[id] == 0:
            continue
        for i in range(id+1, id+1+card_dict[id]):
            if i in card_dict:
                card_stack.append(i)

    print(ncards)

def p2(filename):
    lines = utils.read_file(filename)
    cards = [read_card(l) for l in lines]
    cards = {id: (w, o) for (id, w, o) in cards}
    ncards = len(cards)
    ncards_each = [0] + ([1] * ncards)

    for i in range(1, 1+ncards):
        w, o = cards[i]
        nwins = len(set(w).intersection(set(o)))
        for j in range(min(ncards+1, i+1), min(ncards+1, i+1+nwins)):
            ncards_each[j] += ncards_each[i]
            
    print(sum(ncards_each))


p1('inputs/4.real.txt')
p2('inputs/4.real.txt')