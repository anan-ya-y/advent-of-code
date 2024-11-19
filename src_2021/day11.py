import utils
import numpy as np
WINDOW = np.array([(i, j) for i in range(-1, 2) for j in range(-1, 2) if not i == j == 0])

def perform_day(map):
    map = map + 1
    # for each 10 in the map, increment the window
    flashed = set()
    while True: # we break when flashed doesn't increase more
        flashing = np.where(map >= 10)
        flashing_set = set(zip(*flashing))
        if len(flashing_set) == len(flashed): # no new flashing
            break

        new_flashing = flashing_set - flashed
        for i, j in new_flashing:
            this_window = WINDOW + (i, j)
            # prune window for bounds
            this_window = this_window[(this_window[:, 0] >= 0) & (this_window[:, 0] < map.shape[0])]
            this_window = this_window[(this_window[:, 1] >= 0) & (this_window[:, 1] < map.shape[1])]

            # increment window
            map[this_window[:, 0], this_window[:, 1]] += 1
        flashed = flashing_set
    
    # turn the flashing ones to zeros
    map[flashing] = 0
    return map


def main(input):
    input = utils.split_and_strip(input)
    octopi = np.zeros((len(input), len(input[0])), dtype=int)   
    for i in range(len(input)):
        for j in range(len(input[i])):
            octopi[i, j] = int(input[i][j] )
    noctopi = octopi.shape[0] * octopi.shape[1]
    
    # for i in range(100):
    nflashes = []
    while len(nflashes) <= 100 or nflashes[-1] != noctopi:
        octopi = perform_day(octopi)
        nflashes.append(np.sum(octopi == 0))

    return sum(nflashes[:100]), len(nflashes)


    
    