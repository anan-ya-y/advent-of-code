import utils

def get_value(card, part=1):
    if card.isdigit():
        return int(card)
    if card == "T":
        return 10
    if card == "J":
        return 11 if part==1 else 1
    if card == "Q":
        return 12
    if card == "K":
        return 13
    if card == "A":
        return 14
    return -1

def binary_sort(arr, part=1):
    if len(arr) == 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    bs_left = binary_sort(left, part)
    bs_right = binary_sort(right, part)

    arr = []
    # Merge the two arrays:
    while len(bs_left) > 0 and len(bs_right) > 0:
        if hand_greater(bs_right[0], bs_left[0], part): # right is better than left
            arr.append(bs_left.pop(0))
        else:
            arr.append(bs_right.pop(0))
    while len(bs_left) > 0:
        arr.append(bs_left.pop(0))
    while len(bs_right) > 0:
        arr.append(bs_right.pop(0))

    return arr

def get_hand_type(hand, part=1):
    # count hand contents
    hand_contents = {}
    max_card = 0
    for card in hand:
        if card in hand_contents:
            hand_contents[card] += 1
        else:
            hand_contents[card] = 1
        if max_card == 0 or hand_contents[card] > hand_contents[max_card]:
            if part==1 or (part == 2 and card != "J"):
                max_card = card

    if part == 2 and "J" in hand_contents and max_card != 0:
        # Add Js to our most frequent card
        hand_contents[max_card] += hand_contents["J"]
        del hand_contents["J"]
    if part == 2 and "J" in hand_contents and max_card == 0:
        max_card = "J" # The deck is just 5 Js

    # get ranking. 5 = best, 0 = worst
    if hand_contents[max_card] == 5:
        return 6
    if hand_contents[max_card] == 4:
        return 5
    if hand_contents[max_card] == 3:
        if len(hand_contents.keys()) == 2:
            return 4
        return 3
    if hand_contents[max_card] == 2:
        if len(hand_contents.keys()) == 3:
            return 2
        return 1
    return 0

# return True if hand1 > hand2 else return False
def hand_greater(hand1, hand2, part=1):
    # this is the guts
    h1type = get_hand_type(hand1, part)
    h2type = get_hand_type(hand2, part)
    if h1type != h2type:
        return h1type > h2type
    
    # go char by char
    for i in range(len(hand1)):
        h1c = hand1[i]
        h2c = hand2[i]
        # they are letters
        if h1c != h2c:
            return get_value(h1c, part) > get_value(h2c, part)
        # They are the same card
        continue
    return False

def p1(input):
    lines = utils.split_and_strip(input)
    hb = dict((l.split(" ")[0], l.split(" ")[1]) for l in lines)
    hands = list(hb.keys())

    ranking = binary_sort(hands)
    
    winnings = 0
    for i in range(len(ranking)):
        winnings += (i+1) * int(hb[ranking[i]])

    return winnings

def p2(input):
    lines = utils.split_and_strip(input)
    hb = dict((l.split(" ")[0], l.split(" ")[1]) for l in lines)
    hands = list(hb.keys())

    ranking = binary_sort(hands, part=2)

    winnings = 0
    for i in range(len(ranking)):
        winnings += (i+1) * int(hb[ranking[i]])
    
    return winnings