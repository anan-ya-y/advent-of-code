import pytest, os, json
ANSWER_FILENAME = "tests/answers.json"


import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import runner_utils as ru

def pytest_addoption(parser):
    parser.addoption("--year", action="store", help="run all combinations")

def pytest_generate_tests(metafunc):
    if "questiondata" in metafunc.fixturenames:
        year = metafunc.config.getoption("year")
        if year:
            years = [year]
        else:
            years = [2015, 2016, 2022, 2023]#range(2015, 2024)

        days = range(1, 26)

        question_data = []
        for y in years:
            modules = get_thisyear_modules(y)
            answers = get_answers(y)
            for d in days:
                question_data.append((y, d, modules, answers))
        metafunc.parametrize("questiondata", question_data)

## HELPER FNS
def get_thisyear_modules(year):
    modules = {}
    for i in range(1, 26):
        try:
            m = ru.import_module(year, i)
            modules[i] = m
        except ModuleNotFoundError:
            print("Module not found for year", year, "day", i)
            continue
    return modules

def get_answers(year):
    if not os.path.exists(ANSWER_FILENAME):
        answers = {}
    with open(ANSWER_FILENAME, "r") as f:
        answers = json.load(f)

    if str(year) not in answers:
        return {}
    return answers[str(year)]