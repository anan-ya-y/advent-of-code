import utils
from operator import mul
from functools import reduce
import re

def parse_input(input):
    input = utils.split_and_strip(input)
    robots = [] # (px, py, vx, vy)
    for i in input:
        x, y, vx, vy = map(int, re.findall(r"-?\d+", i))
        robots.append((x, y, vx, vy))
    return robots

def get_position(px, py, vx, vy, t, xbound, ybound):
    return (px + vx * t) % xbound, (py + vy * t) % ybound

def print_map(robot_positions, xbound, ybound):
    grid = [["." for _ in range(xbound)] for _ in range(ybound)]
    for r in robot_positions:
        grid[r[1]][r[0]] = "x"
    for row in grid:    
        print("".join(row))
    

def main(inp):
    robots = parse_input(inp)
    xbound, ybound = 101, 103

    quadrants = [[0, 0], [0, 0]]
    for r in robots:
        end_pos = get_position(*r, 100, xbound, ybound)

        if end_pos[0] == xbound // 2 or end_pos[1] == ybound // 2:
            continue

        xquadrant = 0 if end_pos[0] < xbound // 2 else 1
        yquadrant = 0 if end_pos[1] < ybound // 2 else 1
        quadrants[xquadrant][yquadrant] += 1


    quadrants = quadrants[0] + quadrants[1]

    p2 = -1
    for i in range(10000):
        if i % 103 == 19 and i % 101 == 70:
            print(i)
        else:
            continue
        robot_pos = []
        for r in robots:
            robot_pos.append(get_position(*r, i, xbound, ybound))
        print_map(robot_pos, xbound, ybound)
        # input(f"Above was {i}")
        p2 = i
        break

    return reduce(mul, quadrants, 1), p2

