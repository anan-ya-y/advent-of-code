import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import runner_utils as ru

# def test_compute(setup, year):
#     print(year)

def test_one_day(questiondata):
    year, day, modules, answers = questiondata
    print("Testing", year, day)
    if day not in modules:
        assert False, f"Day {day} not found"
    if str(day) not in answers:
        assert False, f"Day {day} not in correct answers json"
    p1, p2 = ru.run_day(modules[day], year, day, sample=False)
    corrects = answers[str(day)]

    assert p1 == corrects["a"], f"Day {day} part a failed"
    assert p2 == corrects["b"], f"Day {day} part b failed"


