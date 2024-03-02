import importlib
import argparse
import aocd
import os
import time


def get_input_filename(year, day, sample=False):
    if sample:
        filepath = "src_" + str(year) + "/inputs/"+str(day)+".sample.txt"
    else:
        filepath = "src_" + str(year) + "/inputs/"+str(day)+".real.txt"

    if os.path.exists(filepath):
        print("file exists. opening. ")
        return filepath
    elif not sample:
        with open(filepath, "w") as f:
            f.write(aocd.get_data(day=day, year=year))
    else:
        print("No sample input file found for day", day)
        exit(1)
    return filepath

def get_input_string(filename):
    with open(filename, "r") as f:
        return f.read()    


def run_day(year, day, sample=False):
    print("Day", day)
    m = modules[day]
    filename = get_input_filename(year, day, sample)
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

def submit_day(year, day):
    p1, p2 = run_day(year, day, sample=False)
    aocd.submit(p1, part="a", day=day, year=year)
    if p2 is not None:
        aocd.submit(p2, part="b", day=day, year=year)

def import_module(year, day):
    lib = "src_{}.day{}".format(year, day)
    m = globals()[lib] = importlib.import_module(lib)
    # print("Successfuly imported", lib)
    return m

#--------- RUN CODE ----------#

# argument parsing
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("year", type=int, help="Year of AoC")
parser.add_argument("day", nargs="?", type=int, help="Select just one day to run")
parser.add_argument("-s", "--sample", action="store_true", help="Run sample instead of input")
parser.add_argument("-r", "--submit", action="store_true", help="Submit solutions to AoC")
parser.add_argument("-a", "--all", action="store_true", help="run all ")

args = parser.parse_args()

# module importing
modules = {}
if args.day is not None: # importing one specific module
    m = import_module(args.year, args.day)
    modules[args.day] = m
else: # importing all modules
    for i in range(1, 26):
        try:
            m = import_module(args.year, i)
            modules[i] = m
        except ModuleNotFoundError:
            print("Module not found for day", i)
            continue

if args.all:
    print("--AoC {}--\n".format(args.year))
    for i in range(1, len(modules)+1):
        run_day(args.year, i, args.sample)
        print()
else:

    if args.submit:
        submit_day(args.year, args.day)
    else:
        run_day(args.year, args.day, args.sample)

