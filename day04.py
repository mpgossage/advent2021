"""
Advent of Code 2021: day 4
"""
import pytest
from helper import *


def load_bingo(fname):
    with open(fname) as f:
        l = f.readline()
        nums = [int(a) for a in l.split(",")]
        l = f.readline()

        boards = []

        while True:
            # read 5x5
            board = []
            for i in range(5):
                l = f.readline()
                if len(l) <= 1:
                    # tricky to break out of double loop, so just return
                    return (nums, boards)
                board.append([int(a) for a in l.split()])
            boards.append(board)
            l = f.readline()


def count_items_to_win(nums, board):
    "returns the number of 'nums' we need to get though for 'board' to win"
    # a list of all possible ways to win
    wins = []
    for i in range(5):
        w = set()
        w2 = set()
        for j in range(5):
            w.add(board[i][j])
            w2.add(board[j][i])
        wins += [w, w2]
    # each set is the list of items to win

    # play game
    for i in range(len(nums)):
        n = nums[i]
        # remove from each item
        for w in wins:
            w.discard(n)
            if len(w) == 0:
                return i


def calculate_score(nums, board, count):
    s = set()
    for b in board:
        s |= set(b)
    # remove all called items
    called = set(nums[: count + 1])
    s -= called
    return nums[count] * sum(s)


def day04a(fname):
    nums, boards = load_bingo(fname)
    board, count = None, len(nums) + 1
    # all boards and the counts
    counts = ((b, count_items_to_win(nums, b)) for b in boards)
    # best board & count
    best = min(counts, key=lambda a: a[1])
    # score
    return calculate_score(nums, best[0], best[1])


def day04b(fname):
    nums, boards = load_bingo(fname)
    board, count = None, len(nums) + 1
    # all boards and the counts
    counts = ((b, count_items_to_win(nums, b)) for b in boards)
    # best board & count (last to win)
    best = max(counts, key=lambda a: a[1])
    # score
    return calculate_score(nums, best[0], best[1])


################################################################
if __name__ == "__main__":
    print("day04a", day04a("input04.txt"))
    print("day04b", day04b("input04.txt"))

################################################################


def test_load_bingo():
    nums, boards = load_bingo("test04.txt")
    assert len(nums) == 27
    assert nums[0] == 7
    assert nums[1] == 4
    assert nums[26] == 1
    assert len(boards) == 3
    assert boards[0][0][0] == 22
    assert boards[0][4][0] == 1
    assert boards[0][0][4] == 0
    assert boards[0][4][4] == 19


def test_count_items_to_win():
    nums, boards = load_bingo("test04.txt")
    assert count_items_to_win(nums, boards[2]) == 11
    assert count_items_to_win(nums, boards[0]) > 11
    assert count_items_to_win(nums, boards[1]) > 11


def test_calculate_score():
    nums, boards = load_bingo("test04.txt")
    count = count_items_to_win(nums, boards[2])
    assert calculate_score(nums, boards[2], count) == 4512


def test_day04a():
    assert day04a("test04.txt") == 4512


def test_day04b():
    assert day04b("test04.txt") == 1924
