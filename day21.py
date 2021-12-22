"""
Advent of Code 2021: day 21

This looks like a great time to play with generators.
It looks simple enough (at least for now)

Part B is a monster, quantum die here we come, infinite possiblities

Its also the first day I needed to google for help.
It turns out I built my code badly, so a rewrite from scratch fixed it.
"""
import pytest
from helper import *


def load_game(fname):
    "return (start1,start2)"
    return [int(l.split(":")[1]) for l in load_strings(fname)]


def deterministic_dice():
    while True:
        for i in range(1, 101):
            yield i


def take_turn(pos, dice):
    roll = next(dice) + next(dice) + next(dice)
    pos += roll
    pos %= 10
    if pos == 0:
        pos = 10
    return pos


def play_game(p1, p2, dice):
    s1, s2 = 0, 0
    WIN = 1000
    rolls = 0
    while True:
        p1 = take_turn(p1, dice)
        s1 += p1
        rolls += 3
        if s1 >= WIN:
            break
        p2 = take_turn(p2, dice)
        s2 += p2
        rolls += 3
        if s2 >= WIN:
            break
    return s1, s2, rolls


def day21a(fname):
    p1, p2 = load_game(fname)
    dice = deterministic_dice()
    s1, s2, rolls = play_game(p1, p2, dice)
    return min(s1, s2) * rolls


"""
To solve quantum states we have a dict of states:
{(p1,p2,s1,s2):occurences}

for example: if there is only once state
{(1,1,0,0):1}
there are 27 different rolls for 3 dice, but not all unique.

3 is only possible one way (1,1,1)
4 has 3 ways (1,1,2),(1,2,1),(2,1,1)
5 has 6 ways (1,1,3),(1,3,1),(3,1,1),(1,2,2),(2,1,2),(2,2,1)
6 has 7 ways (1,2,3),(1,3,2),(2,3,1),(2,1,3),(3,1,2),(3,2,1),(2,2,2)
7 has 6 ways (2,2,3),(2,3,2),(3,2,2),(1,3,3),(3,1,3),(3,3,1)
8 has 3 ways (2,3,3),(3,2,3),(3,3,2)
9 has 1 way (3,3,3)

So p1 who is on square 1 can be at:
4:1, 5:3, 6:6, 7:7, 8:6, 9:3, 10:1
so we can represent this as a set of states, instead of all 27 versions

The theory is good, but the implmentation fell over horribly.
No idea why.
When the result numbers are 15 digit numbers (500 terra) its not easy to trace why it broke.

So went and looked at:
https://www.reddit.com/r/adventofcode/comments/rl6p8y/2021_day_21_solutions/hpkx49s/

and built a much simpler/more compact set of code which worked
"""


def play_qgame(p1, p2, goal):
    """
    Takes the 2 starting places & the goal, returns the number of wins for p1 & p2.
    """
    # this is a good idea: setting all values first
    # also never seen making a dict using list comprehension before
    states = {
        (x, y, z, w): 0
        for x in range(1, 11)
        for y in range(1, 11)
        for z in range(0, goal)
        for w in range(0, goal)
    }
    # this is inspired: letting python calculate the probabilities
    roll3d3 = [x + y + z for x in range(1, 4) for y in range(1, 4) for z in range(1, 4)]
    dirac_probs = {r: roll3d3.count(r) for r in roll3d3}
    states[(p1, p2, 0, 0)] = 1
    p1win, p2win = 0, 0

    while max(states.values()) != 0:
        for (p1, p2, s1, s2), value in states.items():
            if value == 0:
                continue
            states[(p1, p2, s1, s2)] = 0
            # p1 moves
            for m1, v1 in dirac_probs.items():
                np1 = (p1 + m1 - 1) % 10 + 1
                ns1 = s1 + np1
                if ns1 >= goal:
                    p1win += value * v1
                else:
                    # p2 moves
                    for m2, v2 in dirac_probs.items():
                        np2 = (p2 + m2 - 1) % 10 + 1
                        ns2 = s2 + np2
                        if ns2 >= goal:
                            p2win += value * v1 * v2
                        else:
                            states[(np1, np2, ns1, ns2)] += value * v1 * v2
    return p1win, p2win


def day21b(fname):
    p1, p2 = load_game(fname)
    p1win, p2win = play_qgame(p1, p2, 21)
    return max(p1win, p2win)


################################################################
if __name__ == "__main__":
    print("day21a", day21a("input21.txt"))
    print("day21b", day21b("input21.txt"))

################################################################


def test_load_game():
    assert load_game("test21.txt") == [4, 8]


def test_take_turn():
    p1, p2 = 4, 8
    dice = deterministic_dice()
    p1 = take_turn(p1, dice)
    assert p1 == 10
    p2 = take_turn(p2, dice)
    assert p2 == 3
    p1 = take_turn(p1, dice)
    assert p1 == 4
    p2 = take_turn(p2, dice)
    assert p2 == 6
    p1 = take_turn(p1, dice)
    assert p1 == 6
    p2 = take_turn(p2, dice)
    assert p2 == 7
    p1 = take_turn(p1, dice)
    assert p1 == 6
    p2 = take_turn(p2, dice)
    assert p2 == 6


def test_day21a():
    assert day21a("test21.txt") == 739785


def test_quantum():
    p1win, p2win = play_qgame(4, 8, 21)
    print("p1", p1win, "p2", p2win)
    assert p1win == 444356092776315
    assert p2win == 341960390180808


def test_day21b():
    assert day21b("test21.txt") == 444356092776315
