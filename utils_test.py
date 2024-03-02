import pytest
# to run, just type `pytest` in the terminal

import utils

def test_add():
    assert 1 + 1 == 2

def test_bitmask_set():
    # copilot is writing this test in bits and pieces
    legend = ["a", "b", "c", "d"]

    s1 = set(["a", "c"])
    b1 = utils.set_to_bitmask(s1, legend)
    assert b1 == 5
    assert utils.bitmask_to_set(b1, legend) == s1

    s2 = set(["a", "b", "c", "d"])
    b2 = utils.set_to_bitmask(s2, legend)
    assert b2 == 15
    assert utils.bitmask_to_set(b2, legend) == s2
