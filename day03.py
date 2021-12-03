"""
Advent of Code 2021: day 3
"""
import pytest
from helper import *


def count_digit(arr, index):
    one, zero = 0, 0
    for a in arr:
        if a[index] == "1":
            one += 1
        else:
            zero += 1
    return zero, one


def compute_coef(arr):
    gamma, epsilon = 0, 0

    ln = len(arr[0])
    for i in range(ln):
        z, o = count_digit(arr, i)
        gamma *= 2
        epsilon *= 2
        if o > z:
            gamma += 1
        else:
            epsilon += 1
    return gamma, epsilon


def day03a(fname):
    arr = load_strings(fname)
    g, e = compute_coef(arr)
    return g * e


def filter_array(arr, bMostCommon):
    ln = len(arr[0])
    for i in range(ln):
        ##        print(f"step {i} num {len(arr)}")
        z, o = count_digit(arr, i)
        if bMostCommon:
            if o >= z:
                keep = "1"
            else:
                keep = "0"
        else:
            if o < z:
                keep = "1"
            else:
                keep = "0"
        arr = [a for a in arr if a[i] == keep]
        ##        print(f"end-step {i} num {len(arr)}")
        if len(arr) < 2:
            break

    # should have only one left: convert to int
    val = 0
    for i in range(ln):
        val *= 2
        if arr[0][i] == "1":
            val += 1
    return val


def day03b(fname):
    arr = load_strings(fname)
    return filter_array(arr, True) * filter_array(arr, False)


################################################################
if __name__ == "__main__":
    print("day03a", day03a("input03.txt"))
    print("day03b", day03b("input03.txt"))

################################################################


def test_count_digit():
    arr = load_strings("test03.txt")
    assert count_digit(arr, 0) == (5, 7)
    assert count_digit(arr, 1) == (7, 5)


def test_compute_coef():
    arr = load_strings("test03.txt")
    assert compute_coef(arr) == (22, 9)


def test_day03a():
    assert day03a("test03.txt") == 198


def test_filter_array():
    arr = load_strings("test03.txt")
    assert filter_array(arr, True) == 23
    assert filter_array(arr, False) == 10


def test_day03b():
    assert day03b("test03.txt") == 230
