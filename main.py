import importlib
import argparse
import aocd
import os
import time


def get_input_filename(day, sample=False):
    if sample:
        filepath = "inputs/"+str(day)+".sample.txt"
    else:
        filepath = "inputs/"+str(day)+".real.txt"

    if os.path.exists(filepath):
        print("file exists. opening. ")
        return filepath
    elif not sample:
        with open(filepath, "w") as f:
            f.write(aocd.get_data(day=day, year=2022))
    else:
        print("No sample input file found for day", day)
        exit(1)
    return filepath

def get_input_string(filename):
    with open(filename, "r") as f:
        return f.read()    


def run_day(day, sample=False):
    print("Day", day)
    m = modules[day]
    filename = get_input_filename(day, sample)
    input = get_input_string(filename)

    p1_stime = time.time()
    p1_ans = m.p1(input)
    p1_etime = time.time()
    print("Part 1:\t", p1_ans, "\t", round(p1_etime-p1_stime, 5), "s")

    p2_stime = time.time()
    p2_ans = m.p2(input)
    p2_etime = time.time()
    print("Part 2:\t", p2_ans, "\t", round(p2_etime-p2_stime, 5), "s")

    return p1_ans, p2_ans

def submit_day(day):
    p1, p2 = run_day(day, sample=False)
    aocd.submit(p1, part="a", day=day, year=2022)
    if p2 is not None:
        aocd.submit(p2, part="b", day=day, year=2022)


#--------- RUN CODE ----------#
# module importing
modules = {}
for i in range(1, 26):
    lib = "day"+str(i)
    try:
        m = globals()[lib] = importlib.import_module(lib)
        modules[i] = m
    except:
        pass

# argument parsing
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("day", nargs="?", type=int, help="Select just one day to run")
parser.add_argument("-s", "--sample", action="store_true", help="Run sample instead of input")
parser.add_argument("-r", "--submit", action="store_true", help="Submit solutions to AoC")
parser.add_argument("-a", "--all", action="store_true", help="run all ")

args = parser.parse_args()

if args.all:
    print("--AoC 2023--\n")
    for i in range(1, len(modules)+1):
        run_day(i, args.sample)
        print()
else:

    if args.submit:
        submit_day(args.day)
    else:
        run_day(args.day, args.sample)

