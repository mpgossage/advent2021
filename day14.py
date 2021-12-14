"""
Advent of Code 2021: day 14

This looks potentially hard. Part A is ok,
but part B could become a nightmare if they ask for 1000 iteration or similar.

Part B only asks for 40 iterations, but the length of string over over 2 trillion
So we need a new design
"""
import pytest
from helper import *


def load_polymer(fname):
    """Loads and returns (base,{rules})
    where base is start string and a rule is {"AB":"C"}
    """
    rules = {}
    base = None
    for line in load_strings(fname):
        if base == None:
            base = line
        arr = line.split(" -> ")
        if len(arr) == 2:
            rules[arr[0]] = arr[1]
    return (base, rules)


def grow_polymer(base, rules):
    "returns a grown polymer"
    prev = None
    pair = ""
    result = ""
    for b in base:
        if prev != None:
            pair = prev + b
        if pair in rules:
            result += rules[pair]
        result += b
        prev = b
    return result


def multi_grow_polymer(base, rules, iterations):
    poly = base
    for i in range(iterations):
        poly = grow_polymer(poly, rules)
    return poly


def count_occurance(poly):
    "returns map of {cell:occurance}"
    result = {}
    for p in poly:
        if p not in result:
            result[p] = 0
        result[p] += 1
    return result


def day14a(fname):
    base, rules = load_polymer(fname)
    poly = multi_grow_polymer(base, rules, 10)
    occ = count_occurance(poly)
    # the the biggest & smallest values
    minc = min(occ, key=occ.get)
    maxc = max(occ, key=occ.get)
    return occ[maxc] - occ[minc]


def _grow_and_count_to_poly(base):
    "internal fn for testing: splits the base poly into tokens"
    poly = {}
    for i in range(len(base) - 1):
        pair = base[i : i + 2]
        if pair not in poly:
            poly[pair] = 0
        poly[pair] += 1
    return poly


def _grow_and_count_grow(poly, rules):
    result = {}
    for p, v in poly.items():
        p1 = p[0] + rules[p]
        p2 = rules[p] + p[1]
        if p1 not in result:
            result[p1] = 0
        if p2 not in result:
            result[p2] = 0
        result[p1] += v
        result[p2] += v
    return result


def grow_and_count(base, rules, iteration):
    """Optimised version of the grow & count.
    idea: "NNCB" is {"NN":1,"NC":1,"CB":1}
    with the rule "NN -> C"
    "NN" => "NC":1 and "CN":1
    but if there 1000 of "NN"
    "NN":1000 => "NC":1000 and "CN":1000
    When it gets to counting, we only need to consider the first value of each pair
    Plus the very last letter ("B") which never changes.

    This is a pretty big change, but the unit tests should be able to help this
    """
    poly = _grow_and_count_to_poly(base)

    # generate
    for i in range(iteration):
        poly = _grow_and_count_grow(poly, rules)

    # count
    result = {}
    for p, v in poly.items():
        c = p[0]
        if c not in result:
            result[c] = 0
        result[c] += v
    c = base[-1]
    if c not in result:
        result[c] = 0
    result[c] += 1
    return result


def day14b(fname):
    base, rules = load_polymer(fname)
    occ = grow_and_count(base, rules, 40)
    # the the biggest & smallest values
    minc = min(occ, key=occ.get)
    maxc = max(occ, key=occ.get)
    return occ[maxc] - occ[minc]


################################################################
if __name__ == "__main__":
    print("day14a", day14a("input14.txt"))
    print("day14b", day14b("input14.txt"))

################################################################


def test_load_polymer():
    base, rules = load_polymer("test14.txt")
    assert base == "NNCB"
    assert len(rules) == 16
    assert rules["CH"] == "B"
    assert rules["CN"] == "C"


def test_grow_polymer():
    base, rules = load_polymer("test14.txt")
    poly1 = grow_polymer(base, rules)
    assert poly1 == "NCNBCHB"
    poly2 = grow_polymer(poly1, rules)
    assert poly2 == "NBCCNBBBCBHCB"
    poly3 = grow_polymer(poly2, rules)
    assert poly3 == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    poly4 = grow_polymer(poly3, rules)
    assert poly4 == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"


def test_count_occurance():
    base, rules = load_polymer("test14.txt")
    poly = multi_grow_polymer(base, rules, 10)
    assert len(poly) == 3073
    occ = count_occurance(poly)
    assert occ["B"] == 1749
    assert occ["C"] == 298
    assert occ["H"] == 161
    assert occ["N"] == 865


def test_day14a():
    assert day14a("test14.txt") == 1588


def test_grow_and_count():
    base, rules = load_polymer("test14.txt")
    # check it counts for no work
    occ = grow_and_count(base, rules, 0)
    assert occ == {"N": 2, "C": 1, "B": 1}
    # check some steps
    occ = grow_and_count(base, rules, 1)
    assert occ == {"B": 2, "C": 2, "H": 1, "N": 2}
    occ = grow_and_count(base, rules, 2)
    assert occ == {"B": 6, "C": 4, "H": 1, "N": 2}
    # check the 10 steps
    occ = grow_and_count(base, rules, 10)
    assert occ["B"] == 1749
    assert occ["C"] == 298
    assert occ["H"] == 161
    assert occ["N"] == 865
    # now 40
    occ = grow_and_count(base, rules, 40)
    assert occ["B"] == 2192039569602
    assert occ["H"] == 3849876073


def test_grow_and_count_parts():
    base, rules = load_polymer("test14.txt")
    # check bits:
    poly = _grow_and_count_to_poly(base)
    assert poly == {"NN": 1, "NC": 1, "CB": 1}

    # test grow
    result = _grow_and_count_grow(poly, rules)
    assert result["NC"] == 1
    assert result["CN"] == 1
    assert result["NB"] == 1
    assert result["BC"] == 1
    assert result["CH"] == 1
    assert result["HB"] == 1


def test_day14b():
    assert day14b("test14.txt") == 2188189693529
