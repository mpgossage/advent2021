"""
Advent of Code 2021: day 1
"""
import pytest
from helper import *

def count_increasing(arr):
    if len(arr) < 2: return 0
    total = 0
    val = arr[0]
    for a in arr:
        if a>val:
##            print(f"{a} > {val}")
            total+=1
        val=a
    return total

def day01a(fname):
    return count_increasing(load_ints(fname))

def count_increasing3(arr):
    total = 0
    val = sum(arr[0:3])
    for i in range(len(arr)-2):
        newv=sum(arr[i:i+3])
        if newv>val:
##            print(f"{newv} > {val}")
            total+=1
        val=newv
    return total

def day01b(fname):
    return count_increasing3(load_ints(fname))


if __name__ == "__main__":
    print("day01a", day01a("input01.txt"))
    print("day01b", day01b("input01.txt"))

def test_count_increasing():
    arr = []
    assert count_increasing(arr) == 0
    arr = [199]
    assert count_increasing(arr) == 0
    arr = [199,200]
    assert count_increasing(arr) == 1
    arr = [199,200,199]
    assert count_increasing(arr) == 1
    arr = [199,200,208,210,200,207,240,269,260,263]
    assert count_increasing(arr) == 7

def test_day01a():
    result = day01a("test01.txt")
    assert result == 7

def test_day01b():
    result = day01b("test01.txt")
    assert result == 5
