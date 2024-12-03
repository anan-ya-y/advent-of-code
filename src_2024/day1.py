import utils
import numpy as np

def main(input):
    input = utils.split_and_strip(input)

    l1, l2 = [], []
    for i in input:
        i = list(map(int, i.split()))
        l1.append(i[0])
        l2.append(i[1])
    
    l1 = np.array(l1)
    l2 = np.array(l2)

    l1.sort()
    l2.sort()

    frequencies = {}
    for i in l1:
        if i in frequencies:
            continue
        frequencies[i] = np.sum(l2 == i)
        
    return np.sum(np.abs(l1-l2)), sum([frequencies[x]*x for x in l1])
