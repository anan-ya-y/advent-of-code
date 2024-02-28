import utils 

shapes = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
    "A": "rock", 
    "B": "paper",
    "C": "scissors"
}

def getshapescore(shape):
    word_shape = shapes[shape]
    if word_shape == "rock":
        return 1
    if word_shape == "paper":
        return 2
    if word_shape == "scissors":
        return 3

def getwinscore(p_them, p_us):
    shape_them = shapes[p_them]
    shape_us = shapes[p_us]
    if shape_them == shape_us: # draw
        return 3
    if shape_them == "rock" and shape_us == "paper":
        return 6
    if shape_them == "scissors" and shape_us == "rock":
        return 6
    if shape_them == "paper" and shape_us == "scissors":
        return 6
    # lose case
    return 0

def getmove(p_them, strat): # I don't care about readability.
    if strat == "Y": # draw
        return p_them
    if strat == "X": # lose
        if p_them == "A":
            return "C"
        if p_them == "B":
            return "A"
        if p_them == "C":
            return "B"
    if strat == "Z": # win
        if p_them == "A":
            return "B"
        if p_them == "B":
            return "C"
        if p_them == "C":
            return "A"


def p1(input):
    lines = utils.split_and_strip(input)
    points = 0
    for l in lines:
        p_them, p_us = l.strip().split(" ")
        shape = getshapescore(p_us)
        win = getwinscore(p_them, p_us)
        points += (shape+win)

    return points

def p2(input):
    lines = utils.split_and_strip(input)
    points = 0
    for l in lines:
        p_them, strat = l.strip().split(" ")
        p_us = getmove(p_them, strat)
        shape = getshapescore(p_us)
        win = getwinscore(p_them, p_us)
        points += (shape+win)

    return points

    