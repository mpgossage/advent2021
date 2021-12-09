"""
Advent of Code 2021: day 9

Part A is simple, part B looks a little more complex,
but I feel like I want to visualise this, so I'm going to add extra code to visualize it
"""
import pytest
from helper import *


def find_lowest_points(grid):
    result = []
    my, mx = len(grid), len(grid[0])
    for y in range(my):
        for x in range(mx):
            # is this lowest
            lowest = True
            if y > 0 and grid[y][x] >= grid[y - 1][x]:
                lowest = False
            if y < my - 1 and grid[y][x] >= grid[y + 1][x]:
                lowest = False
            if x > 0 and grid[y][x] >= grid[y][x - 1]:
                lowest = False
            if x < mx - 1 and grid[y][x] >= grid[y][x + 1]:
                lowest = False
            if lowest:
                result.append((x, y))
    return result


def day09a(fname):
    grid = load_digit_grid(fname)
    lowest = find_lowest_points(grid)
    count = 0
    for lx, ly in lowest:
        ##        print(f"Low {lx},{ly} {grid[ly][lx]}")
        count += grid[ly][lx] + 1
    return count


def fill(grid, x, y, val):
    "4 way flood grid[y][x] and areas around it with new value val"
    # note: iterative version could be used if this is too slow
    my, mx = len(grid), len(grid[0])
    oldval = grid[y][x]
    grid[y][x] = val
    if y > 0 and grid[y - 1][x] == oldval:
        fill(grid, x, y - 1, val)
    if y < my - 1 and grid[y + 1][x] == oldval:
        fill(grid, x, y + 1, val)
    if x > 0 and grid[y][x - 1] == oldval:
        fill(grid, x - 1, y, val)
    if x < mx - 1 and grid[y][x + 1] == oldval:
        fill(grid, x + 1, y, val)


def flood_basins(grid):
    """
    given a grid, flood fill across the grid marking all the basins.
    return will be 0 if grid == 9 else 1+ depending upon basin
    """
    my, mx = len(grid), len(grid[0])
    result = make_int_grid(mx, my, -1)
    # setup all the grid==9 as 0
    for y in range(my):
        for x in range(mx):
            if grid[y][x] == 9:
                result[y][x] = 0
    # flood all the -1's
    count = 0
    for y in range(my):
        for x in range(mx):
            if result[y][x] == -1:
                count += 1
                fill(result, x, y, count)
    return result


def print_flood(grid):
    for line in grid:
        for c in line:
            if c == 0:
                print(".", end="")
            else:
                print(c % 10, end="")
        print()


def count_basins(grid):
    "returns the size of the basins"
    result = {}
    for line in grid:
        for c in line:
            if c > 0:
                if c not in result:
                    result[c] = 0
                result[c] += 1
    return list(result.values())


def day09b(fname):
    grid = load_digit_grid(fname)
    result = flood_basins(grid)
    counted = count_basins(result)
    counted.sort(reverse=True)
    return counted[0] * counted[1] * counted[2]


################################################################
if __name__ == "__main__":
    print("day09a", day09a("input09.txt"))
    print("day09b", day09b("input09.txt"))

################################################################


def test_find_lowest_points():
    grid = load_digit_grid("test09.txt")
    lowest = find_lowest_points(grid)
    assert len(lowest) == 4
    assert (1, 0) in lowest
    assert (9, 0) in lowest
    assert (2, 2) in lowest
    assert (6, 4) in lowest


def test_day09a():
    assert day09a("test09.txt") == 15


def test_flood_basins():
    grid = load_digit_grid("test09.txt")
    result = flood_basins(grid)
    show = False
    if show:
        print("grid")
        print_flood(grid)
        print("flood")
        print_flood(result)
        assert False  # make an error and the output is shown
    # not doing a big test for this. using visual instead
    assert result[0][0] == 1
    assert result[1][0] == 1
    assert result[2][0] == 0


def test_count_basins():
    grid = load_digit_grid("test09.txt")
    result = flood_basins(grid)
    counted = count_basins(result)
    assert len(counted) == 4
    # cannot be sure of ordering
    assert sorted(counted) == [3, 9, 9, 14]


def test_day09b():
    assert day09b("test09.txt") == 1134
