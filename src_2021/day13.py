import utils
import numpy as np


def main(input):
    input = utils.split_and_strip(input, "\n\n")
    just_coords = utils.split_and_strip(input[0], "\n")
    just_coords = np.array([list(map(int, x.split(","))) for x in just_coords])

    instructions = np.zeros((max(just_coords[:, 0]) + 1, max(just_coords[:, 1]) + 1)).T

    instructions[just_coords[:, 1], just_coords[:, 0]] = 1

    p1 = -1
    for inst in input[1].split("\n"):
        inst = inst.split()[-1].split("=")
        axis = inst[0]
        val = int(inst[1])

        if axis == "y":
            nrows = instructions.shape[0]
            new_size = (max(nrows-val-1, val+1), instructions.shape[1])
            new_instructions = np.zeros(new_size)
            new_instructions = instructions[:val, :]
            print(f"{val=}")
            new_instructions[new_size[0]-val-1:, :] += instructions[val+1::, :][::-1, :]
            instructions = new_instructions
        else:
            ncols = instructions.shape[1]
            new_size = (instructions.shape[0], max(ncols-val-1, val+1))
            new_instructions = np.zeros(new_size)
            new_instructions = instructions[:, :val]
            print("left shape:", new_instructions[:, new_size[1]-val-1:].shape)
            print("right shape",  instructions[:, val+1::][:, ::-1].shape)
            print(f"{val=}")
            new_instructions[:, new_size[1]-val-1:] += instructions[:, val+1::][:, ::-1]
            instructions = new_instructions

        if p1 == -1:
            p1 = np.sum(instructions > 0)
            print(p1)
        
    for r in instructions:
        print("".join(["#" if x >= 1 else "." for x in r]))
    return p1, -1
