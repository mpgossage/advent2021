"""
Advent of Code 2021: day 7

Part B needed a big refactor as the cost function changed a lot.

Therefore refactored find_best_pos & calculate_cost to take a costfn.
Instead of duplicating the code.
This is really simple with all the unit tests to make sure I didn't break anything
"""
import pytest
from helper import *


def calculate_cost(crabs, tgt, costfn):
    """calculates and returns the cost of getting all crabs to tgt"""
    return sum((costfn(c - tgt) for c in crabs))


def find_best_pos(crabs, costfn):
    "returns (best pos, best cost)"
    # assuming that all positions from 0..mx
    # we could attempt to optimise, but its not needed
    mx = max(crabs)
    # all costs
    costs = [(i, calculate_cost(crabs, i, costfn)) for i in range(mx)]
    best = min(costs, key=lambda c: c[1])
    return best


def day07a(fname):
    crabs = load_ints_csv_line(fname)
    result = find_best_pos(crabs, abs)
    return result[1]


def crab_fuel_cost(v):
    "part B fuel cost function"
    v = abs(v)
    return (v + 1) * v // 2


def day07b(fname):
    crabs = load_ints_csv_line(fname)
    result = find_best_pos(crabs, crab_fuel_cost)
    return result[1]


################################################################
if __name__ == "__main__":
    print("day07a", day07a("input07.txt"))
    print("day07b", day07b("input07.txt"))

################################################################


def test_calculate_cost():
    crabs = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert calculate_cost(crabs, 2, abs) == 37
    assert calculate_cost(crabs, 1, abs) == 41
    assert calculate_cost(crabs, 3, abs) == 39
    assert calculate_cost(crabs, 10, abs) == 71


def test_find_best_pos():
    crabs = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert find_best_pos(crabs, abs) == (2, 37)


def test_crab_fuel_cost():
    assert crab_fuel_cost(1) == 1
    assert crab_fuel_cost(2) == 3
    assert crab_fuel_cost(3) == 6
    assert crab_fuel_cost(16 - 5) == 66
    assert crab_fuel_cost(1 - 5) == 10


def test_calculate_cost2():
    crabs = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert calculate_cost(crabs, 2, crab_fuel_cost) == 206
    assert calculate_cost(crabs, 5, crab_fuel_cost) == 168


def test_find_best_pos():
    crabs = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert find_best_pos(crabs, crab_fuel_cost) == (5, 168)


def test_day07a():
    assert day07a("test07.txt") == 37


def test_day07b():
    result = day07b("test07.txt")
    assert result == 168
