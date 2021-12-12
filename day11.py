"""
Advent of Code 2021: day 11

This is looking like a fun day.
Going to need some drawing for this one.
Lots of unit tests for check some simple cases and more complex cases.
"""
import pytest
from helper import *


def sim_grid(grid):
    "given a grid, advances the grid one cycle and returns the number of flashes"
    my, mx = len(grid), len(grid[0])
    flashed = set()
    toflash = set()

    for y in range(my):
        for x in range(mx):
            grid[y][x] += 1
            if grid[y][x] > 9:
                toflash.add((x, y))

    while len(toflash) > 0:
        f = toflash.pop()
        if f in flashed:
            continue
        flashed.add(f)
        fx, fy = f
        # calc flash area(inclusive)
        x1, x2 = max(fx - 1, 0), min(fx + 1, mx - 1)
        y1, y2 = max(fy - 1, 0), min(fy + 1, my - 1)
        ##        print(f"flash {fx},{fy} area {x1},{y1}=>{x2},{y2}")
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                grid[y][x] += 1
                if grid[y][x] > 9:
                    toflash.add((x, y))

    for fx, fy in flashed:
        grid[fy][fx] = 0

    return len(flashed)


def print_grid(grid):
    for line in grid:
        print("".join((str(l) for l in line)))


def count_flashes(grid, gen):
    count = 0
    for g in range(gen):
        count += sim_grid(grid)
    return count


def day11a(fname):
    grid = load_digit_grid(fname)
    return count_flashes(grid, 100)


def find_sync_gen(grid):
    my, mx = len(grid), len(grid[0])
    gen = 0
    while True:
        gen += 1
        if sim_grid(grid) == mx * my:
            return gen


def day11b(fname):
    grid = load_digit_grid(fname)
    return find_sync_gen(grid)


################################################################
if __name__ == "__main__":
    print("day11a", day11a("input11.txt"))
    print("day11b", day11b("input11.txt"))

################################################################


def test_sim_grid_trivial():
    # trivial, non flashing items
    grid = [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
    assert sim_grid(grid) == 0
    assert grid[0][0] == 1
    assert grid[1][1] == 2
    assert grid[2][2] == 3


def test_sim_grid_flash():
    # simple flash, not overlapping
    grid = [[9, 0, 0, 0], [1, 1, 9, 1], [2, 2, 2, 2]]
    assert sim_grid(grid) == 2
    print_grid(grid)
    # flashed are zero
    assert grid[0][0] == 0
    assert grid[1][2] == 0
    # some just inc
    assert grid[2][0] == 3
    # single flash area (1 +1 inc, +1 flash)
    assert grid[1][0] == 3
    # double flash area (1 +1 inc, +2 flashes)
    assert grid[1][1] == 4


def test_sim_grid_corner():
    # simple flash, checking corner cases
    grid = [[9, 0, 9], [0, 0, 0], [9, 0, 9]]
    assert sim_grid(grid) == 4
    print_grid(grid)
    assert grid[0][0] == 0
    assert grid[0][2] == 0
    assert grid[2][0] == 0
    assert grid[2][2] == 0
    assert grid[1][1] == 5


def test_sim_grid_ripple():
    """ripple flash from example
    11111   34543
    19991   40004
    19191   50005
    19991   40004
    11111   34543"""
    grid = [
        [1, 1, 1, 1, 1],
        [1, 9, 9, 9, 1],
        [1, 9, 1, 9, 1],
        [1, 9, 9, 9, 1],
        [1, 1, 1, 1, 1],
    ]
    assert sim_grid(grid) == 9
    assert grid[0] == [3, 4, 5, 4, 3]
    assert grid[1] == [4, 0, 0, 0, 4]
    assert grid[2] == [5, 0, 0, 0, 5]
    assert grid[3] == [4, 0, 0, 0, 4]
    assert grid[4] == [3, 4, 5, 4, 3]

    assert sim_grid(grid) == 0
    assert grid[0] == [4, 5, 6, 5, 4]
    assert grid[1] == [5, 1, 1, 1, 5]
    assert grid[2] == [6, 1, 1, 1, 6]
    assert grid[3] == [5, 1, 1, 1, 5]
    assert grid[4] == [4, 5, 6, 5, 4]


def test_sim_grid_test11():
    "using the example given, not checking cells, just checking flashes"
    grid = load_digit_grid("test11.txt")
    print("\ngen0")
    print_grid(grid)

    print("\ngen1")
    assert sim_grid(grid) == 0
    print_grid(grid)

    print("\ngen2")
    assert sim_grid(grid) == 35
    print_grid(grid)

    print("\ngen3")
    assert sim_grid(grid) == 45
    print_grid(grid)

    print("\ngen4")
    assert sim_grid(grid) == 16
    print_grid(grid)


def test_count_flashes():
    grid = load_digit_grid("test11.txt")
    assert count_flashes(grid, 10) == 204
    grid = load_digit_grid("test11.txt")
    assert count_flashes(grid, 100) == 1656


def test_day11a():
    assert day11a("test11.txt") == 1656


def test_day11b():
    assert day11b("test11.txt") == 195
