"""
Advent of Code 2021: day 6

As expected when I looked at part A of the question,
the part B would be for a large number number of generations where the simple method would not work.
"""
import pytest
from helper import *


def sim_generation(fish):
    """Deliberately simplistic simulate fish generation.
    Will probably be used for compare to later versions
    (it wasn't)"""
    result = []
    spawn = 0
    for f in fish:
        if f == 0:
            result.append(6)
            spawn += 1
        else:
            result.append(f - 1)
    for i in range(spawn):
        result.append(8)
    return result


def count_generations(fish, gen):
    for g in range(gen):
        fish = sim_generation(fish)
    return len(fish)


def day06a(fname):
    fish = load_ints_csv_line(fname)
    return count_generations(fish, 80)


def state_to_counts(fish):
    """converts an array of fish to a list of counts.
    eg. [3,4,3,1,2] => [0,1,1,2,1,0,0,0,0]
    each value in the array is the number of fish which have this count.
    eg. [0,1,1,2,1,0,0,0,0] is one '1' one '2' two '3's one '4' and no other fish
    """
    result = [0] * 9
    for f in fish:
        result[f] += 1
    return result


def sim_state(counts, gen):
    """Simulates 'gen' generations on fish 'counts'
    this is much simpler and uses a fixed size array
    Every 2 becomes a 1, every 6 becomes a 5
    Every 0 becomes a 6 & an 8 (new spawn).
    This can probably be optimised more, but lets just try this method.
    """
    for g in range(gen):
        f0 = counts[0]
        # this is the indexes 1,2,3,4,5,6,7,8,0
        # moving stuff down
        counts = counts[1:] + [f0]
        counts[6] += f0
    return counts


def count_generations2(fish, gen):
    "optimised version of count_generations"
    return sum(sim_state(state_to_counts(fish), gen))


def day06b(fname):
    fish = load_ints_csv_line(fname)
    return count_generations2(fish, 256)


####################################################################
if __name__ == "__main__":
    print("day06a", day06a("input06.txt"))
    print("day06b", day06b("input06.txt"))

##################################################################


def test_sim_generation():
    assert sim_generation([3, 4, 3, 1, 2]) == [2, 3, 2, 0, 1]
    assert sim_generation([2, 3, 2, 0, 1]) == [1, 2, 1, 6, 0, 8]
    assert sim_generation([1, 2, 1, 6, 0, 8]) == [0, 1, 0, 5, 6, 7, 8]
    assert sim_generation([0, 1, 0, 5, 6, 7, 8]) == [6, 0, 6, 4, 5, 6, 7, 8, 8]


def test_count_generations():
    assert count_generations([3, 4, 3, 1, 2], 1) == 5
    assert count_generations([3, 4, 3, 1, 2], 18) == 26
    assert count_generations([3, 4, 3, 1, 2], 80) == 5934
    # code will not test and cannot get an answer in 60 seconds
    # not suprising as it needs to make an array of almost 27 billion items


##    assert count_generations([3,4,3,1,2],256) == 26984457539


def test_day06a():
    assert day06a("test06.txt") == 5934


def test_state_to_counts():
    assert state_to_counts([3, 4, 3, 1, 2]) == [0, 1, 1, 2, 1, 0, 0, 0, 0]
    assert state_to_counts([]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert state_to_counts([3, 4, 3, 1, 2, 8, 8, 8, 8, 0, 0, 0]) == [
        3,
        1,
        1,
        2,
        1,
        0,
        0,
        0,
        4,
    ]


def test_count_generations2():
    assert count_generations2([3, 4, 3, 1, 2], 1) == 5
    assert count_generations2([3, 4, 3, 1, 2], 18) == 26
    assert count_generations2([3, 4, 3, 1, 2], 80) == 5934
    assert count_generations2([3, 4, 3, 1, 2], 256) == 26984457539
