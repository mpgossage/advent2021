"""
Advent of Code 2021: helpers
"""


def load_ints(fname):
    with open(fname) as f:
        return [int(l) for l in f.readlines()]

def load_strings(fname):
    "no test, its trivial"
    with open(fname) as f:
        return f.readlines()


def test_load_ints():
    arr = load_ints("test01.txt")
    assert len(arr) == 10
    assert arr[0]==199
    assert arr[1]==200
    assert arr[9]==263
