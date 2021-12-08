"""
Advent of Code 2021: day 8

Reading this puzzle was a definate WAT! moment.
This looks like its going to be hard.

Part A I can do with just basic checking lengths, so stupidly doing this.
I doubt thats going to help in the overall scheme, just lets just clear A.

As expected part B is going to need a full solve, which is going to take some serious thought.

Turns out you don't need to figure out the segment locations, just the segments=>number
Which is a chunk easier, see determine_mapping()
"""
import pytest
from helper import *


def parse_line(line):
    """converts
    acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    into a pair of arrays.
    Sorting all strings for each of matching"""
    arr = line.split(" | ")
    return (arr[0].split(" "), arr[1].split(" "))


def detect_unique(digits):
    """given an array of digits, returns the unique digits (1,4,7,8)"""
    return [d for d in digits if len(d) in [2, 3, 4, 7]]


def day08a(fname):
    lines = [parse_line(l) for l in load_strings(fname)]
    ##    count = 0
    ##    for l in lines:
    ##        un = detect_unique(l[1])
    ##        print(l[1],un)
    ##        count+=len(un)
    ##    return count
    return sum((len(detect_unique(l[1])) for l in lines))


def count_overlap(a, b):
    "returns the number of segments of 'a' which overlap with 'b'"
    return sum((1 for c in a if c in b))


def determine_mapping(digits):
    """
    given the array of digits return a map(str=>int) of the mappings.
    Rules: (see https://adventofcode.com/2021/day/8#part2 for segment mappings)
    2 segments => 1
    3 segments => 7
    4 segments => 4
    7 segments => 8
    6 segments and does not light up all of 1's segments (cf) => 6
    6 segments and does not light up all of 4's segments (bcdf) => 0
    6 segments & not yet matched => 9
    5 segments and lights up all of 1's segments (cf) => 3
    finally compare overlap between remainder & 4's segments (bcdf)
    2 overlapping segments (cd) => 2
    3 overlapping segments (bdf) => 5

    Will use helper fn: count_overlap

    """
    mapping = {}
    # easy mappings first
    for d in digits:
        ln = len(d)
        if ln == 2:
            d1 = d
        if ln == 3:
            d7 = d
        if ln == 4:
            d4 = d
        if ln == 7:
            d8 = d
    # 6 segs
    segment6 = [d for d in digits if len(d) == 6]
    # find the 6
    for s in segment6:
        if count_overlap(s, d1) != 2:
            d6 = s
    # find the 4
    segment6.remove(d6)
    for s in segment6:
        if count_overlap(s, d4) != 4:
            d0 = s
    # 9 is remainder
    segment6.remove(d0)
    d9 = segment6[0]

    # 5 segs
    segment5 = [d for d in digits if len(d) == 5]
    # find the 3
    for s in segment5:
        if count_overlap(s, d1) == 2:
            d3 = s
    segment5.remove(d3)
    # final 2 & 5
    for s in segment5:
        c = count_overlap(s, d4)
        if c == 2:
            d2 = s
        else:
            d5 = s

    return {d0: 0, d1: 1, d2: 2, d3: 3, d4: 4, d5: 5, d6: 6, d7: 7, d8: 8, d9: 9}


def order_token(token):
    "orders a string token alphabetically"
    return "".join(sorted(list(token)))


def lookup_value(segments, mapping):
    # rebuild mapping to be ordered:
    smapping = {}
    for k, v in mapping.items():
        smapping[order_token(k)] = v
    result = 0
    for s in segments:
        result = result * 10 + smapping[order_token(s)]
    return result


def day08b(fname):
    lines = [parse_line(l) for l in load_strings(fname)]
    count = 0
    for l in lines:
        mapping = determine_mapping(l[0])
        count += lookup_value(l[1], mapping)
    return count


################################################################
if __name__ == "__main__":
    print("day08a", day08a("input08.txt"))
    print("day08b", day08b("input08.txt"))

################################################################


def test_parse_line():
    a, b = parse_line(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    )
    assert len(a) == 10
    assert len(b) == 4
    assert a[0] == "acedgfb"
    assert a[9] == "ab"
    assert b[0] == "cdfeb"
    assert b[3] == "cdbaf"


def test_detect_unique():
    a = detect_unique("fdgacbe cefdb cefbgd gcbe".split())
    print(a)
    assert a == ["fdgacbe", "gcbe"]


def test_day08a():
    assert day08a("test08.txt") == 26


def test_count_overlap():
    assert count_overlap("abcd", "ab") == 2
    assert count_overlap("abcd", "a") == 1
    assert count_overlap("abcd", "aefgh") == 1
    assert count_overlap("abc", "xyz") == 0
    assert count_overlap("ab", "abcd") == 2


def test_determine_mapping():
    a, b = parse_line(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    )
    mapping = determine_mapping(a)
    assert mapping["ab"] == 1
    assert mapping["dab"] == 7
    assert mapping["eafb"] == 4
    assert mapping["acedgfb"] == 8
    assert mapping["cdfgeb"] == 6
    assert mapping["cagedb"] == 0
    assert mapping["cefabd"] == 9
    assert mapping["cdfbe"] == 5
    assert mapping["gcdfa"] == 2
    assert mapping["fbcad"] == 3


def test_lookup_value():
    a, b = parse_line(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    )
    mapping = determine_mapping(a)
    assert lookup_value(b, mapping) == 5353


def test_day08b():
    assert day08b("test08.txt") == 61229
