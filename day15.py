"""
Advent of Code 2021: day 15

Looks like a simple day, breath first search, at least for part A.
Part B is interesting as its the map that changes.
Part B took ~3 seconds to compute which was getting slightly concerning
"""
import pytest
from heapq import heappush, heappop
from helper import *

ADJACENT = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def navigate_grid(grid):
    my, mx = len(grid), len(grid[0])
    # using a simple best first search
    # grid with lowest costs & paths in a priority queue
    max_cost = 9 * (my + mx)
    costs = make_grid(mx, my, max_cost)
    costs[0][0] = 0  # always free
    # queue format is (cost,[(px,py)...])
    todo = []
    heappush(todo, (0, [(0, 0)]))
    while todo:
        c, path = heappop(todo)
        px, py = path[-1]
        # found path to end
        if px == mx - 1 and py == my - 1:
            return c, path
        # check adjacent
        for ax, ay in ADJACENT:
            tx, ty = px + ax, py + ay
            if 0 <= tx < mx and 0 <= ty < my:
                newc = c + grid[ty][tx]
                if newc < costs[ty][tx]:
                    costs[ty][tx] = newc
                    newp = path + [(tx, ty)]
                    heappush(todo, (newc, newp))
    # should never return
    assert "error"


def day15a(fname):
    return navigate_grid(load_digit_grid(fname))[0]


def expand_grid(grid):
    my, mx = len(grid), len(grid[0])
    newg = make_grid(mx * 5, my * 5, 0)
    for y in range(my * 5):
        for x in range(mx * 5):
            dx, rx = divmod(x, mx)
            dy, ry = divmod(y, my)
            t = grid[ry][rx] + dx + dy
            if t > 9:
                t -= 9
            newg[y][x] = t
    return newg


def day15b(fname):
    grid = expand_grid(load_digit_grid(fname))
    return navigate_grid(grid)[0]


################################################################
if __name__ == "__main__":
    print("day15a", day15a("input15.txt"))
    print("day15b", day15b("input15.txt"))

################################################################


def test_navigate_grid():
    grid = load_digit_grid("test15.txt")
    cost, path = navigate_grid(grid)
    assert cost == 40
    assert len(path) == 19
    assert path[0] == (0, 0)
    assert path[2] == (0, 2)
    assert path[8] == (6, 2)
    assert path[10] == (7, 3)
    assert path[13] == (8, 5)
    assert path[17] == (9, 8)
    assert path[18] == (9, 9)


def test_expand_grid():
    grid = load_digit_grid("test15.txt")
    exgrid = expand_grid(grid)
    assert len(exgrid) == 50
    assert len(exgrid[0]) == 50
    l0 = "".join((str(i) for i in exgrid[0]))
    assert l0 == "11637517422274862853338597396444961841755517295286"
    l49 = "".join((str(i) for i in exgrid[49]))
    assert l49 == "67554889357866599146897761125791887223681299833479"


def test_day15b():
    assert day15b("test15.txt") == 315
