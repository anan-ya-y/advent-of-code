import utils
import numpy as np
import scipy as sp

c = complex
DIRECTIONS = [
    c(-1, -1), 
    c(-1, 0), 
    c(-1, 1), 
    c(0, -1), 
    c(0, 1), 
    c(1, -1), 
    c(1, 0), 
    c(1, 1)
]


def get_valid_paper_pos(printerroom):
    nneighbors = sp.signal.convolve2d(printerroom, np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), mode="same", boundary="fill")
   
    neighbor_positions = np.argwhere(nneighbors < 4)
    paper_roll_positions = np.argwhere(printerroom == 1)
    all_paper = set(map(tuple, neighbor_positions)).intersection(set(map(tuple, paper_roll_positions)))
    
    return all_paper


def main(input):
    inp = utils.split_and_strip(input)
    
    printerroom = np.zeros((len(inp), len(inp[0])), dtype=int)

    for l in range(len(inp)):
        line = inp[l]
        for i in range(len(line)):
            if line[i] == "@":
                printerroom[l][i] = 1
    
    p1 = len(get_valid_paper_pos(printerroom))

    p2 = 0
    while True:
        paper_positions = get_valid_paper_pos(printerroom)
        if len(paper_positions) == 0:
            break

        p2 += len(paper_positions)
        for p in paper_positions:
            printerroom[p] = 0


    return p1, p2


