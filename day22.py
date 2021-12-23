"""
Advent of Code 2021: day 22

This looks like a fairly fun day.
An infinite grid, will use a simple set to hold all cells which are on.
Part A is only 500K cells which a set will easily hold, but if I add all the cells listed.
we get over 21 Terra cells which is going to break stuff.
(the last line is 21T alone)

Going to skip this & just solve the simple problem first.
Will worry about the part B later.

Found test22b (500K cubes took ~5 seconds to process)

Part B was as expected, we are going to need a new algol to handle this.

Basic algol is going to be a subtract cuboid(A,B) which returns cubioid A with B removes from it.
If A & B do not overlap, it will return A
If A is inside B it will return Nothing
If there is partial overlap it will return a set of cuboids whish is A-B

eg. given
 +-----------------------+
 | A                     |
 |                       |
 |                       |
 |     +-------+         |
 |     | B     |         |
 |     |       |         |
 +-----|       |---------+
       |       |          
       +-------+          
Will return A1,A2,A3
 +-----+-------+---------+
 | A1  | A2    | A3      |
 |     |       |         |
 |     |       |         |
 |     +-------+         |
 |     |       |         |
 |     |       |         |
 +-----+       +---------+

Took a while to build and a few issues with debugging, but overall not too bad. 
"""
import pytest
from helper import *


def load_cubes(fname):
    "load puzzle. returns [(on/off,x1,x2,y1,y2,z1,z2)]"
    cubes = []
    for l in load_strings(fname):
        l = (
            l.replace("x=", " ")
            .replace(",y=", " ")
            .replace(",z=", " ")
            .replace("..", " ")
        )
        a = l.split()
        on = a[0] == "on"
        c = [int(v) for v in a[1:]]
        cubes.append(tuple([on] + c))
    return cubes


def count_cubes(cubes):
    cells = set()
    for on, x1, x2, y1, y2, z1, z2 in cubes:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if on:
                        cells.add((x, y, z))
                    else:
                        cells.discard((x, y, z))
    return len(cells)


def day22a(fname):
    cubes = load_cubes(fname)
    # filter
    cubes = [c for c in cubes if min(c[1:]) >= -50 and max(c[1:]) <= 50]
    return count_cubes(cubes)


def sub_cuboid(cube_a, cube_b):
    "returns [(cubes)] of cube_a without cube_b"
    ax1, ax2, ay1, ay2, az1, az2 = cube_a
    bx1, bx2, by1, by2, bz1, bz2 = cube_b
    # if not connected, then return [a]
    if bx1 > ax2 or bx2 < ax1 or by1 > ay2 or by2 < ay1 or bz1 > az2 or bz2 < az1:
        return [cube_a]
    # if A is fully inside B return []
    if (
        ax1 >= bx1
        and ax2 <= bx2
        and ay1 >= by1
        and ay2 <= by2
        and az1 >= bz1
        and az2 <= bz2
    ):
        return []
    # its partial overlap, split accodingly
    result = []
    # we check if we can cut of a section, if we can we add that section & reduce main body
    if ax1 < bx1:
        result.append((ax1, bx1 - 1, ay1, ay2, az1, az2))
        ax1 = bx1
    if ax2 > bx2:
        result.append((bx2 + 1, ax2, ay1, ay2, az1, az2))
        ax2 = bx2
    if ay1 < by1:
        result.append((ax1, ax2, ay1, by1 - 1, az1, az2))
        ay1 = by1
    if ay2 > by2:
        result.append((ax1, ax2, by2 + 1, ay2, az1, az2))
        ay2 = by2
    if az1 < bz1:
        result.append((ax1, ax2, ay1, ay2, az1, bz1 - 1))
        az1 = bz1
    if az2 > bz2:
        result.append((ax1, ax2, ay1, ay2, bz2 + 1, az2))
        az2 = bz2

    return result


def count_cubes2(cubes):
    "improved version of count cubes using the sub_cuboid code"
    result = []
    for c in cubes:
        on, cube = c[0], c[1:]
        if on:
            # we need to take the new cuboid and remove all existing items
            to_add = [cube]
            for existing in result:
                to_add = sum((sub_cuboid(add, existing) for add in to_add), [])
            result += to_add
        else:
            # for removal, all existing have this removed
            result = sum((sub_cuboid(r, cube) for r in result), [])
    # now count the cells
    return sum(
        (
            (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
            for x1, x2, y1, y2, z1, z2 in result
        )
    )


def day22b(fname):
    cubes = load_cubes(fname)
    return count_cubes2(cubes)


################################################################
if __name__ == "__main__":
    print("day22a", day22a("input22.txt"))
    print("day22b", day22b("input22.txt"))

################################################################


def test_load_cubes():
    cubes = load_cubes("test22a.txt")
    assert len(cubes) == 4
    assert cubes[0][0] == True
    assert cubes[1][0] == True
    assert cubes[2][0] == False
    assert cubes[3][0] == True
    assert cubes[0] == (True, 10, 12, 10, 12, 10, 12)


def test_count_cubes():
    cubes = load_cubes("test22a.txt")
    assert count_cubes(cubes) == 39


def test_day22a():
    assert day22a("test22a.txt") == 39
    # commenting 22b as its too slow


##    assert day22a("test22b.txt") == 590784


def test_sub_cuboid_simple():
    # A & B not overlap
    A = (0, 10, 0, 10, 0, 10)
    B = (15, 20, 0, 10, 0, 10)
    assert sub_cuboid(A, B) == [A]
    assert sub_cuboid(A, (-5, -1, 0, 10, 0, 10)) == [A]
    assert sub_cuboid(A, (0, 10, 11, 20, 0, 10)) == [A]
    assert sub_cuboid(A, (0, 10, -5, -1, 0, 10)) == [A]
    assert sub_cuboid(A, (0, 10, 0, 10, 11, 20)) == [A]
    assert sub_cuboid(A, (0, 10, 0, 10, -5, -1)) == [A]
    # A inside B
    assert sub_cuboid(A, A) == []
    assert sub_cuboid(A, (-5, 20, -5, 20, -5, 20)) == []


def test_sub_cuboid():
    # simple cut part of A with a large B on the X axis
    A = (0, 10, 0, 10, 0, 10)
    B = (5, 50, 0, 10, 0, 10)
    assert sub_cuboid(A, B) == [(0, 4, 0, 10, 0, 10)]
    B = (-10, 5, 0, 10, 0, 10)
    assert sub_cuboid(A, B) == [(6, 10, 0, 10, 0, 10)]
    # Y axis
    B = (0, 10, 5, 50, 0, 10)
    assert sub_cuboid(A, B) == [(0, 10, 0, 4, 0, 10)]
    B = (0, 10, -10, 5, 0, 10)
    assert sub_cuboid(A, B) == [(0, 10, 6, 10, 0, 10)]
    # Z axis
    B = (0, 10, 0, 10, 5, 50)
    assert sub_cuboid(A, B) == [(0, 10, 0, 10, 0, 4)]
    B = (0, 10, 0, 10, -10, 5)
    assert sub_cuboid(A, B) == [(0, 10, 0, 10, 6, 10)]

    # a corner of B is insize A should give 3 cubes
    B = (5, 50, 5, 50, 5, 50)
    assert sub_cuboid(A, B) == [
        (0, 4, 0, 10, 0, 10),
        (5, 10, 0, 4, 0, 10),
        (5, 10, 5, 10, 0, 4),
    ]

    # B is inside A so we get 6 cuboids
    B = (4, 6, 4, 6, 4, 6)
    assert sub_cuboid(A, B) == [
        (0, 3, 0, 10, 0, 10),
        (7, 10, 0, 10, 0, 10),
        (4, 6, 0, 3, 0, 10),
        (4, 6, 7, 10, 0, 10),
        (4, 6, 4, 6, 0, 3),
        (4, 6, 4, 6, 7, 10),
    ]


def test_hand_process_cubes():
    # hand processing this to make sure the algol is good
    cubes = load_cubes("test22a.txt")
    assert len(cubes) == 4
    c1 = cubes[0][1:]
    c2 = cubes[1][1:]
    c3 = cubes[2][1:]
    c4 = cubes[3][1:]

    def print_cells(cubes):
        "helper fn to get the full list of cells & show them"
        cells = []
        for x1, x2, y1, y2, z1, z2 in cubes:
            cells += (
                (x, y, z)
                for x in range(x1, x2 + 1)
                for y in range(y1, y2 + 1)
                for z in range(z1, z2 + 1)
            )
        cells.sort(key=lambda c: c[0] * 1000 + c[1] * 100 + c[2])
        print("total", len(cells))
        for c in cells:
            print(c)

    # 1st cube is there
    result = [c1]
    print("c1 only")
    print_cells(result)
    # 2nd cube must have 1st removed
    result += sub_cuboid(c2, c1)
    print("c1 & c2")
    print_cells(result)
    # 3rd is an off, so it subtracts from ALL cubes
    result = sum((sub_cuboid(r, c3) for r in result), [])
    print("removed c3")
    print_cells(result)
    # 4th is an on, but it must have all the other cubes removed from it
    temp = [c4]
    for r in result:
        temp = sum((sub_cuboid(t, r) for t in temp), [])
    result += temp
    print("final")
    print_cells(result)
    # now count all the cubes
    total = sum(
        (
            (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
            for x1, x2, y1, y2, z1, z2 in result
        )
    )
    assert total == 39


def test_count_cubes2():
    cubes = load_cubes("test22a.txt")
    assert count_cubes2(cubes) == 39

    # testing the larger example:
    cubes = load_cubes("test22b.txt")
    cubes = [c for c in cubes if min(c[1:]) >= -50 and max(c[1:]) <= 50]
    assert count_cubes2(cubes) == 590784
