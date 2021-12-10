"""
Advent of Code 2021: day 10
Little concerned on part A.
I'm only handling some of the cases and will have to rebuild the code.
In the end I changed the validate_line to return None, string or list, depending upon the error type
"""
import pytest
from helper import *


def validate_line(line):
    "checks line. returns None for no error, a char if there is syntax error, list for auto correct error"
    CLOSE_LOOKUP = {"(": ")", "[": "]", "{": "}", "<": ">"}
    stack = []
    for l in line:
        if l in "([{<":
            stack.append(l)
        else:
            token = stack.pop()
            if l != CLOSE_LOOKUP[token]:
                return l
    if len(stack) == 0:
        return None
    # make up missing items for auto correct:
    return [CLOSE_LOOKUP[t] for t in reversed(stack)]


def score_illegal_char(c):
    if c == ")":
        return 3
    if c == "]":
        return 57
    if c == "}":
        return 1197
    if c == ">":
        return 25137
    return 0


def score_autocomplete(tokens):
    "given the current stack: calculates the score to complete"
    SCORES = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for t in tokens:
        score *= 5
        score += SCORES[t]
    return score


def day10a(fname):
    score = 0
    for l in load_strings(fname):
        c = validate_line(l)
        if c != None:
            score += score_illegal_char(c)
    return score


def get_median(scores):
    ln = len(scores)
    assert ln % 2 == 1
    scores.sort()
    return scores[ln // 2]


def day10b(fname):
    scores = []
    for l in load_strings(fname):
        err = validate_line(l)
        if type(err) == list:
            scores.append(score_autocomplete(err))
    return get_median(scores)


################################################################
if __name__ == "__main__":
    print("day10a", day10a("input10.txt"))
    print("day10b", day10b("input10.txt"))

################################################################


def test_validate_line_legal():
    # legal first
    assert validate_line("()") == None
    assert validate_line("[]") == None
    assert validate_line("([])") == None
    assert validate_line("{()()()}") == None
    assert validate_line("<([{}])>") == None
    assert validate_line("[<>({}){}[([])<>]]") == None
    assert validate_line("(((((((((())))))))))") == None


def test_validate_line_illegal():
    # illegals
    assert validate_line("(]") == "]"
    assert validate_line("{()()()>") == ">"
    assert validate_line("(((()))}") == "}"
    assert validate_line("<([]){()}[{}])") == ")"


def test_day10a():
    assert day10a("test10.txt") == 26397


def test_score_autocomplete():
    assert score_autocomplete(list("])}>")) == 294
    assert score_autocomplete(list("}}]])})]")) == 288957
    assert score_autocomplete(list(")}>]})")) == 5566
    assert score_autocomplete(list("}}>}>))))")) == 1480781
    assert score_autocomplete(list("]]}}]}]}>")) == 995444
    assert score_autocomplete(list("])}>")) == 294


def test_day10b():
    assert day10b("test10.txt") == 288957
