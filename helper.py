"""
Advent of Code 2021: helpers
"""


def load_ints(fname):
    """
    reads and returns a list of integers from a file,
    one integer per line"""
    with open(fname) as f:
        return [int(l) for l in f.readlines()]


def load_ints_csv_line(fname):
    """
    reads and returns a list of integers from a file,
    single CSV line"""
    with open(fname) as f:
        l = f.readline()
        return [int(n) for n in l.split(",")]


def load_strings(fname):
    with open(fname) as f:
        return [l.strip("\n") for l in f.readlines()]


def make_int_grid(x, y, val):
    return [[val] * x for i in range(y)]


def test_load_ints():
    arr = load_ints("test01.txt")
    assert len(arr) == 10
    assert arr[0] == 199
    assert arr[1] == 200
    assert arr[9] == 263


def test_load_ints_csv_line():
    arr = load_ints_csv_line("test06.txt")
    assert len(arr) == 5
    assert arr[0] == 3
    assert arr[1] == 4
    assert arr[4] == 2


def test_make_int_grid():
    g1 = make_int_grid(1, 2, 3)
    assert len(g1) == 2
    assert len(g1[0]) == 1
    assert g1[0][0] == 3
    assert g1[1][0] == 3
    g2 = make_int_grid(20, 10, 0)
    assert len(g2) == 10
    assert len(g2[9]) == 20
    assert g2[9][19] == 0
