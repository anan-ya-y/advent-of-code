import importlib
import aocd
import os
import time
import numpy as np

# UTILS FILE FOR RUNNING AOCD SOLUTIONS QUICKLY. 
#### FOR OUTPUT CAPTURING. 
# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
import io, contextlib


# FOR ACTUAL AOCD RUNNING. 

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

def run_day(module, year, day, sample=False):
    print("Day", day)
    m = module
    filename = get_input_filename(year, day, sample)
    input = get_input_string(filename)

    if hasattr(m, "p1") and callable(m.p1):
        p1_stime = time.time()
        p1_ans = m.p1(input)
        p1_etime = time.time()
        print("Part 1:\t", p1_ans, "\t", round(p1_etime-p1_stime, 5), "s")

        if hasattr(m, "p2") and callable(m.p2):
            p2_stime = time.time()
            p2_ans = m.p2(input)
            p2_etime = time.time()
            print("Part 2:\t", p2_ans, "\t", round(p2_etime-p2_stime, 5), "s")
        else:
            p2_ans = -1
    else: # run as "main" function with tuple output. 
        stime = time.time()
        p1_ans, p2_ans = m.main(input)
        etime = time.time()
        print("Part 1:\t", p1_ans, "\t", round(etime-stime, 5), "s")
        print("Part 2:\t", p2_ans, "\t", round(etime-stime, 5), "s")

    p1_ans, p2_ans = clean_ans(p1_ans), clean_ans(p2_ans)
    return p1_ans, p2_ans

# return a string, int, or float. 
def clean_ans(ans):
    if type(ans) in [str, int, float]:
        return ans
    if type(ans) in [np.integer, np.int64, np.int32]:
        return int(ans)
    if type(ans) in [np.float64]:
        return float(ans) 
    if ans is None:
        return None
    raise ValueError("Invalid answer type", type(ans))


# returns bool, bool for p1, p2 correct
def submit_day(module, year, day):
    p1, p2 = run_day(module, year, day, sample=False)
    p1_correct =  __submit_ans(p1, "a", day, year)
    if p2 is not None:
        p2_correct = __submit_ans(p2, "b", day, year)
    else:
        p2_correct = day == 25

    return p1, p2, p1_correct, p2_correct

def __submit_ans(ans, part, day, year):
    aocd.submit(ans, part=part, day=day, year=year)
    # f = io.StringIO()
    # with contextlib.redirect_stdout(f):
        # aocd.submit(ans, part=part, day=day, year=year)
    # out = f.getvalue()
    # print(out)
    # return "That's the right answer" in out \
            # or "already solved with same answer" in out

def import_module(year, day):
    lib = "src_{}.day{}".format(year, day)
    m = globals()[lib] = importlib.import_module(lib)
    # print("Successfuly imported", lib)
    return m
