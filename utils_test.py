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

def test_is_prime():
    assert utils.is_prime(1) == False
    assert utils.is_prime(2) == True
    assert utils.is_prime(3) == True
    assert utils.is_prime(4) == False
    assert utils.is_prime(5) == True
    assert utils.is_prime(91) == False
    assert utils.is_prime(97) == True
    assert utils.is_prime(1001) == False
    assert utils.is_prime(111) == False

def test_prime_factorize():
    # copilot wrote this test. 
    assert utils.prime_factorize(1) == []
    assert utils.prime_factorize(2) == [2]
    assert utils.prime_factorize(3) == [3]
    assert utils.prime_factorize(4) == [2, 2]
    assert utils.prime_factorize(5) == [5]
    assert utils.prime_factorize(6) == [2, 3]
    assert utils.prime_factorize(7) == [7]
    assert utils.prime_factorize(8) == [2, 2, 2]
    assert utils.prime_factorize(9) == [3, 3]
    assert utils.prime_factorize(10) == [2, 5]
    assert utils.prime_factorize(11) == [11]
    assert utils.prime_factorize(12) == [2, 2, 3]
    assert utils.prime_factorize(13) == [13]
    assert utils.prime_factorize(14) == [2, 7]
    assert utils.prime_factorize(15) == [3, 5]
    assert utils.prime_factorize(16) == [2, 2, 2, 2]
    assert utils.prime_factorize(17) == [17]
    assert utils.prime_factorize(18) == [2, 3, 3]
    assert utils.prime_factorize(19) == [19]
    assert utils.prime_factorize(20) == [2, 2, 5]
    assert utils.prime_factorize(21) == [3, 7]
    assert utils.prime_factorize(22) == [2, 11]
    assert utils.prime_factorize(23) == [23]
    assert utils.prime_factorize(24) == [2, 2, 2, 3]
    assert utils.prime_factorize(25) == [5, 5]
    assert utils.prime_factorize(26) == [2, 13]
    assert utils.prime_factorize(27) == [3, 3, 3]
    assert utils.prime_factorize(28) == [2, 2, 7]
    assert utils.prime_factorize(29) == [29]
    
def test_num_sum_prod_divisors():
    for i in range(1, 1002):
        num = 0
        sum = 0
        prod = 1
        for j in range(1, i+1):
            if i % j == 0:
                num += 1
                sum += j
                prod *= j
        assert utils.number_of_divisors(i) == num
        assert utils.sum_of_divisors(i) == sum
        if i < 899: # numbers get too big
            assert utils.product_of_divisors(i) == prod

def test_bfs():
    graph = {
        'A': ['B', 'C'],
        'B': ['F'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': ['E']
    }

    x = utils.bfs_with_neighbors(graph, 'A')
    assert x['A'] == 0
    assert x['B'] == 1
    assert x['C'] == 1
    assert 'D' not in x 
    assert x['E'] == 3
    assert x['F'] == 2
    assert utils.bfs_with_neighbors(graph, 'A', 'D') == -1