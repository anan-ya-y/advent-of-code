import numpy as np

def main(input):
    fish = np.array(list(map(int, input.split(","))))
    fish = {i: np.sum(fish == i) for i in range(9)}

    for i in range(1, 256+1):
        # shift all the fish down 1 day
        fish = {j: fish[j+1] for j in range(-1, 8)}
        fish[8] = 0

        # reproduce
        nreproduce = fish[-1]
        fish[6] += nreproduce
        fish[8] += nreproduce
        if i == 80:
            p1 = sum([v for k, v in fish.items() if k >= 0])
    p2 = sum([v for k, v in fish.items() if k >= 0])

    return p1, p2
