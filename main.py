import argparse, json
import runner_utils as ru

ANSWERFILENAME = "tests/answers.json"

def write_ans(existing_answers, year, day, part, ans):
    y = str(year)
    d = str(day)
    if y not in existing_answers:
        existing_answers[y] = {}
    if d not in existing_answers[y]:
        existing_answers[y][d] = {}
    existing_answers[y][d][part] = ans
    return existing_answers

#--------- RUN CODE ----------#

# argument parsing
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("year", type=int, help="Year of AoC")
parser.add_argument("day", nargs="?", type=int, help="Select just one day to run")
parser.add_argument("-s", "--sample", action="store_true", help="Run sample instead of input")
parser.add_argument("-r", "--submit", action="store_true", help="Submit solutions to AoC")
parser.add_argument("-a", "--all", action="store_true", help="run all ")
parser.add_argument("-w", "--write", action="store_true", help=f"write correct answers to {ANSWERFILENAME}")

args = parser.parse_args()

# module importing
modules = {}
if args.day is not None: # importing one specific module
    m = ru.import_module(args.year, args.day)
    modules[args.day] = m
else: # importing all modules
    for i in range(1, 26):
        try:
            m = ru.import_module(args.year, i)
            modules[i] = m
        except ModuleNotFoundError:
            print("Module not found for day", i)
            continue

if args.write:
    # read the json file. 
    with open(ANSWERFILENAME, "r") as f:
        answers = json.load(f)

if args.all:
    days = range(1, len(modules)+1)
    print("--AoC {}--\n".format(args.year))
else:
    days = [args.day]

for d in days:
    if args.submit or args.write:
        p1, p2, p1_correct, p2_correct = ru.submit_day(modules[d], args.year, d)
        if args.write and p1_correct:
            answers = write_ans(answers, args.year, d, "a", p1)
        if args.write and p2_correct:
            answers = write_ans(answers, args.year, d, "b", p2)
    else:
        ru.run_day(modules[d], args.year, d, args.sample)

if args.write:
    with open(ANSWERFILENAME, "w") as f:
        json.dump(answers, f, indent=4)

# if args.all:
#     print("--AoC {}--\n".format(args.year))
#     for i in range(1, len(modules)+1):
#         run_day(args.year, i, args.sample)
#         print()
# else:

#     if args.submit:
#         submit_day(args.year, args.day)
#     else:
#         run_day(args.year, args.day, args.sample)

