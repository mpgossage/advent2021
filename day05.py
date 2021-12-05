"""
Advent of Code 2021: day 5
"""
import pytest
from helper import *


def parse_line(line):
    p1, p2 = line.strip("\n").split(" -> ")
    x1, y1 = (int(a) for a in p1.split(","))
    x2, y2 = (int(a) for a in p2.split(","))
    return (x1, y1, x2, y2)


def load_lines(fname):
    with open(fname) as f:
        return [parse_line(l) for l in f.readlines()]


def is_horizon_vert(line):
    return line[0] == line[2] or line[1] == line[3]


def count_line_max(lines):
    # count max dimentions and create the grid
    maxx1 = max((l[0] for l in lines))
    maxx2 = max((l[2] for l in lines))
    maxy1 = max((l[1] for l in lines))
    maxy2 = max((l[3] for l in lines))
    return (max(maxx1, maxx2) + 1, max(maxy1, maxy2) + 1)


def add_hv_line(line, grid):
    "first version, used in part-a then replaced in part-b"
    x1, y1, x2, y2 = line
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            grid[y][x1] += 1
    else:
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            grid[y1][x] += 1


def sgn(x):
    if x < 0:
        return -1
    if x > 0:
        return +1
    return 0


def add_line(line, grid):
    x1, y1, x2, y2 = line

    steps = max(abs(x1 - x2), abs(y1 - y2)) + 1
    dx = sgn(x2 - x1)
    dy = sgn(y2 - y1)
    x, y = x1, y1
    ##    print(f"line {x1},{y1}->{x2},{y2} Start {x},{y} steps {steps} delta {dx} {dy}")
    for i in range(steps):
        grid[y][x] += 1
        x += dx
        y += dy


def lines_to_grid(lines):
    maxx, maxy = count_line_max(lines)
    grid = make_int_grid(maxx, maxy, 0)
    # fill grid
    for l in lines:
        add_line(l, grid)

    return grid


def count_grid_above(grid, val):
    count = 0
    for g in grid:
        for c in g:
            if c > val:
                count += 1
    return count


def day05a(fname):
    lines = [l for l in load_lines(fname) if is_horizon_vert(l)]
    grid = lines_to_grid(lines)
    return count_grid_above(grid, 1)


def day05b(fname):
    lines = [l for l in load_lines(fname)]
    grid = lines_to_grid(lines)
    return count_grid_above(grid, 1)


def print_grid(grid):
    for g in grid:
        print(g)


##################################################################
if __name__ == "__main__":
    print("day05a", day05a("input05.txt"))
    print("day05b", day05b("input05.txt"))

##################################################################


def test_parse_line():
    assert parse_line("0,9 -> 5,9") == (0, 9, 5, 9)
    assert parse_line("5,5 -> 8,2") == (5, 5, 8, 2)


def test_load_lines():
    lines = load_lines("test05.txt")
    assert len(lines) == 10
    assert len(lines[0]) == 4
    assert lines[0] == (0, 9, 5, 9)
    assert lines[1] == (8, 0, 0, 8)


def test_count_line_max():
    lines = [l for l in load_lines("test05.txt") if is_horizon_vert(l)]
    x, y = count_line_max(lines)
    assert x, y == (10, 10)


def test_lines_to_grid():
    lines = [l for l in load_lines("test05.txt") if is_horizon_vert(l)]
    print(lines)
    grid = lines_to_grid(lines)
    print_grid(grid)
    assert grid[0][0] == 0
    assert grid[1][2] == 1
    assert grid[2][2] == 1
    assert grid[2][2] == 1
    assert grid[9][0] == 2
    assert grid[9][1] == 2
    assert grid[9][2] == 2
    assert grid[9][3] == 1


def test_day05a():
    assert day05a("test05.txt") == 5


def test_day05b():
    assert day05b("test05.txt") == 12
