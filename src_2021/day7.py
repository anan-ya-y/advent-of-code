import numpy as np

def main(input):
    crabs = np.array(list(map(int, input.split(","))))

    p1 = np.inf
    p2 = np.inf
    for i in range(min(crabs), max(crabs)):
        # this decreases then increases so once we hit the inflection point we can quit
        target = i
        fuel_p1 = sum(abs(crabs - target))
        p1 = min(fuel_p1, p1)

        fuel_p2 = abs(crabs-i)
        fuel_p2 = sum(fuel_p2 * (fuel_p2 + 1) / 2)
        p2 = min(fuel_p2, p2)

        if fuel_p1 > p1 and fuel_p2 > p2:
            break

    return p1, p2

