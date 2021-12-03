"""
Advent of Code 2021: day 2
"""
import pytest
from helper import *


def process_line(line):
    cmd, val = line.split(" ")
    val = int(val)
    if cmd == "forward":
        return val, 0
    if cmd == "down":
        return 0, val
    if cmd == "up":
        return 0, -val


def day02a(fname):
    cmds = load_strings(fname)
    x, y = 0, 0
    for c in cmds:
        dx, dy = process_line(c)
        x += dx
        y += dy
    ##        print(f"{c} => {x}, {y}")
    print(f"Final location => {x}, {y}")
    return x * y


def day02b(fname):
    cmds = load_strings(fname)
    x, y, aim = 0, 0, 0
    for c in cmds:
        dx, dy = process_line(c)
        x += dx
        aim += dy
        y += aim * dx
    ##        print(f"{c} => {x}, {y}, {aim}")
    print(f"Final location => {x}, {y}")
    return x * y


################################################################
if __name__ == "__main__":
    print("day02a", day02a("input02.txt"))
    print("day02b", day02b("input02.txt"))

################################################################


def test_process_line():
    assert process_line("forward 5") == (5, 0)
    assert process_line("down 5") == (0, 5)
    assert process_line("up 3") == (0, -3)
    assert process_line("forward 8") == (8, 0)


def test_day02a():
    assert day02a("test02.txt") == 150


def test_day02b():
    assert day02b("test02.txt") == 900
