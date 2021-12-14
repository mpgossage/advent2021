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


def load_digit_grid(fname):
    "loads a file & returns an 2d int grid where each digit is converted to an int"
    result = []
    for l in load_strings(fname):
        result.append([int(c) for c in l])
    return result


# should not have called it an int grid, it can be any kind of grid
# the flexibility of python
def make_int_grid(x, y, val):
    return [[val] * x for i in range(y)]


def make_grid(x, y, val):
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


def test_load_digit_grid():
    grid = load_digit_grid("test09.txt")
    assert len(grid) == 5
    for g in grid:
        assert len(g) == 10
    assert grid[0][0] == 2
    assert grid[0][1] == 1
    assert grid[0][9] == 0
