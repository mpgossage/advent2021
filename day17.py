"""
Advent of Code 2021: day 17

This is going to be fun. Possibly hard, but fun.
I expect to have to use a lot of possible calculations to find good values.
So lets just go exhautive and try.
Not drawing a pretty picture, despite how much I want to.
"""
import pytest
from helper import *
import time


def load_scenario(fname):
    "parses the file and returns (x1,x2,y1,y2)"
    line = load_strings(fname)[0]
    # could regex this, but using replace and then split
    line = line.replace("target area: x=", "").replace(" y=", "")
    line = line.replace("..", ",")
    return [int(v) for v in line.split(",")]


def sim_particle(dx, dy, ymin):
    "simulates and returns a particles path (x,y) until y<ymin (exclusive)"
    path = []
    x, y = 0, 0
    while y >= ymin:
        path.append((x, y))
        x += dx
        y += dy
        dy -= 1
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1
    return path


def hits_target_area(path, area):
    xmin, xmax, ymin, ymax = area
    for p in path:
        if xmin <= p[0] <= xmax and ymin <= p[1] <= ymax:
            return True
    return False


def day17a(fname):
    """
    simplest thing that works:
    dy must be at least 1 as we want height
    just exhastive in some resonable looking ranges
    my first attempt had numbers at the limit, so I had to increase my limit
    adaptive limits would be good.
    This was slow (10 seconds) for 1000 items, but reducing to just 250 made is much quicker
    """
    area = load_scenario(fname)
    ymin = area[2]

    maxht = lambda path: max((p[1] for p in path))
    best_height = -1

    limit = 250
    xlimit = min(limit, area[1])
    for dy in range(1, limit):
        for dx in range(1, xlimit):
            p = sim_particle(dx, dy, ymin)
            if hits_target_area(p, area):
                ht = maxht(p)
                ##                print(f"{dx} {dy} has height {ht}")
                best_height = max(best_height, ht)
    return best_height


def day17b(fname):
    """
    simplest thing that works:
    going exhausive again
    """
    area = load_scenario(fname)

    # ymax from part A
    xmin, xmax = 0, area[1]
    ymin, ymax = area[2], 250

    count = 0
    for dy in range(ymin, ymax):
        for dx in range(xmin, xmax + 1):
            p = sim_particle(dx, dy, ymin)
            if hits_target_area(p, area):
                count += 1
    return count


################################################################
if __name__ == "__main__":
    print("day17a", day17a("input17.txt"))
    start = time.perf_counter()
    print("day17b", day17b("input17.txt"))
    taken = time.perf_counter() - start
    print(f"time taken {taken}")

################################################################


def test_load_scenario():
    assert load_scenario("test17.txt") == [20, 30, -10, -5]


def test_sim_particle():
    assert sim_particle(7, 2, -10) == [
        (0, 0),
        (7, 2),
        (13, 3),
        (18, 3),
        (22, 2),
        (25, 0),
        (27, -3),
        (28, -7),
    ]
    assert sim_particle(6, 3, -10) == [
        (0, 0),
        (6, 3),
        (11, 5),
        (15, 6),
        (18, 6),
        (20, 5),
        (21, 3),
        (21, 0),
        (21, -4),
        (21, -9),
    ]


def test_hits_target_area():
    area = load_scenario("test17.txt")
    assert hits_target_area(sim_particle(7, 2, -10), area) == True
    assert hits_target_area(sim_particle(6, 3, -10), area) == True
    assert hits_target_area(sim_particle(9, 0, -10), area) == True
    assert hits_target_area(sim_particle(17, -4, -10), area) == False

    assert hits_target_area(sim_particle(6, 9, -10), area) == True


def test_day17a():
    assert day17a("test17.txt") == 45


def test_day17b():
    assert day17b("test17.txt") == 112
