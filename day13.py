"""
Advent of Code 2021: day 13

This looks like another fun day.
"""
import pytest
from helper import *


def load_origami(fname):
    """parse the origami file and returns ([dots],[folds])
    where a dot is (X,Y) and a fold is ('X',N)"""

    dots = []
    folds = []
    for line in load_strings(fname):
        if "," in line:
            arr = [int(t) for t in line.split(",")]
            dots.append((arr[0], arr[1]))
        if "=" in line:
            arr = line.replace("fold along ", "").split("=")
            folds.append((arr[0], int(arr[1])))

    return (dots, folds)


def fold_dots(dots, fold):
    "Perfroms a single fold & returns the dots"
    # local fns
    def fold_y(x, y, axis):
        if y < axis:
            return (x, y)
        return (x, 2 * axis - y)

    def fold_x(x, y, axis):
        if x < axis:
            return (x, y)
        return (2 * axis - x, y)

    axis, val = fold
    if axis == "y":
        return [fold_y(d[0], d[1], val) for d in dots]
    if axis == "x":
        return [fold_x(d[0], d[1], val) for d in dots]


def print_dots(dots):
    "prints the dots"
    maxx = max((d[0] for d in dots)) + 1
    maxy = max((d[1] for d in dots)) + 1
    grid = make_grid(maxx, maxy, ".")
    for x, y in dots:
        grid[y][x] = "#"
    for g in grid:
        print("".join(g))


def show_fold(fname, count):
    "display fn show stuff"
    dots, folds = load_origami(fname)

    print("inital")
    print_dots(dots)

    count = min(len(folds), count)
    for c in range(count):
        print("\nfold", 1 + c, folds[c])
        dots = fold_dots(dots, folds[c])
        print_dots(dots)


def day13a(fname):
    "I think part A is throw away, so putting direct into the fn"
    dots, folds = load_origami(fname)
    dots = fold_dots(dots, folds[0])
    # converting to a set which will remove duplicates
    return len(set(dots))


def day13b(fname):
    """Tried using show_fold it takes forever showing all the steps
    no test for this as its visual.
    Could return the arrays & assert on some points, but not really worth the effort
    """

    dots, folds = load_origami(fname)
    for f in folds:
        dots = fold_dots(dots, f)
    print_dots(dots)


################################################################
if __name__ == "__main__":
    ##    show_fold("test13.txt",2)
    print("day13a", day13a("input13.txt"))
    # part B is just show_fold, but show the end state
    day13b("input13.txt")

################################################################


def test_load_origami():
    dots, folds = load_origami("test13.txt")
    assert len(dots) == 18
    assert dots[0] == (6, 10)
    assert dots[-1] == (9, 0)

    assert len(folds) == 2
    assert folds[0] == ("y", 7)
    assert folds[1] == ("x", 5)


def test_fold_dots():
    dots, folds = load_origami("test13.txt")
    dots = fold_dots(dots, folds[0])
    assert (0, 0) in dots
    assert (2, 0) in dots
    assert (3, 0) in dots
    assert (0, 1) in dots


def test_day13a():
    assert day13a("test13.txt") == 17
