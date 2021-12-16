"""
Advent of Code 2021: day 16

This is the day.
This is when the nightmare really begins.
This is going to be hard.

hex to binary then parsing as we go.
We are going to need a full parse tree really.
"""
import pytest
from helper import *
import functools
import operator

ID_SUM = 0
ID_PRODUCT = 1
ID_MIN = 2
ID_MAX = 3
ID_VALUE = 4
ID_GREATER = 5
ID_LESS = 6
ID_EQUALS = 7


def hex2bin(hx):
    "returns hex string to binary string"
    result = ""
    for h in hx:
        i = int(h, 16)  # to int
        result += format(i, "04b")  # to bin
    return result


def parse_header(bstr, idx):
    "parses a binary string header and returns (ver,type,new_idx)"
    ver = int(bstr[idx : idx + 3], 2)
    typ = int(bstr[idx + 3 : idx + 6], 2)
    return ver, typ, idx + 6


def parse_value(bstr, idx):
    "parses a binary string value and returns (value,new_idx)"
    # read the val (going to ignore buffer overflow)
    sval = ""
    while True:
        b = bstr[idx]
        sval += bstr[idx + 1 : idx + 5]
        idx += 5
        if b == "0":
            break
    return int(sval, 2), idx


def parse_tree(bstr, idx):
    """parses a binary string operator and returns a tree"""
    ver, typ, idx = parse_header(bstr, idx)
    if typ == ID_VALUE:
        val, idx = parse_value(bstr, idx)
        return (ver, typ, val), idx

    branches = []
    # its an op
    if bstr[idx] == "0":
        # processing a number of bits
        # number of bits to process
        ln = int(bstr[idx + 1 : idx + 16], 2)
        idx += 16
        eidx = idx + ln
        # lets parse this stuff
        while idx < eidx:
            tree, idx = parse_tree(bstr, idx)
            branches.append(tree)
    else:
        # processing a number of sub-packets
        ln = int(bstr[idx + 1 : idx + 12], 2)
        idx += 12
        for i in range(ln):
            tree, idx = parse_tree(bstr, idx)
            branches.append(tree)

    return (ver, typ, branches), idx


def sum_versions(tree):
    "traverses the tree and returns sum of versions"
    ver, typ, vals = tree
    if typ == ID_VALUE:
        return ver
    # its an op, so sum the versions
    return ver + sum((sum_versions(v) for v in vals))


def day16a(fname):
    bstr = hex2bin(load_strings(fname)[0])
    tree, idx = parse_tree(bstr, 0)
    return sum_versions(tree)


def eval_tree(tree):
    "traverses the tree and returns the value"
    ver, typ, vals = tree
    if typ == ID_VALUE:
        return vals
    if typ == ID_SUM:
        return sum((eval_tree(v) for v in vals))
    if typ == ID_PRODUCT:
        return functools.reduce(operator.mul, (eval_tree(v) for v in vals), 1)
    if typ == ID_MIN:
        return min((eval_tree(v) for v in vals))
    if typ == ID_MAX:
        return max((eval_tree(v) for v in vals))
    if typ == ID_GREATER:
        if eval_tree(vals[0]) > eval_tree(vals[1]):
            return 1
        return 0
    if typ == ID_LESS:
        if eval_tree(vals[0]) < eval_tree(vals[1]):
            return 1
        return 0
    if typ == ID_EQUALS:
        if eval_tree(vals[0]) == eval_tree(vals[1]):
            return 1
        return 0


def day16b(fname):
    bstr = hex2bin(load_strings(fname)[0])
    tree, idx = parse_tree(bstr, 0)
    return eval_tree(tree)


################################################################
if __name__ == "__main__":
    print("day16a", day16a("input16.txt"))
    print("day16b", day16b("input16.txt"))

################################################################


def test_hex2bin():
    assert hex2bin("0") == "0000"
    assert hex2bin("A") == "1010"
    assert hex2bin("D2FE28") == "110100101111111000101000"
    assert (
        hex2bin("38006F45291200")
        == "00111000000000000110111101000101001010010001001000000000"
    )
    assert (
        hex2bin("EE00D40C823060")
        == "11101110000000001101010000001100100000100011000001100000"
    )


def test_parse_header():
    bstr = hex2bin("D2FE28")
    ver, ty, idx = parse_header(bstr, 0)
    assert ver == 6
    assert ty == 4
    assert idx == 6


def test_parse_value():
    bstr = hex2bin("D2FE28")
    ver, ty, idx = parse_header(bstr, 0)
    assert ty == 4
    val, idx = parse_value(bstr, idx)
    assert val == 2021
    assert bstr[idx:] == "000"


def test_parse_tree():
    tree, idx = parse_tree(hex2bin("D2FE28"), 0)
    print("D2FE28", idx, tree)
    assert tree[0] == 6
    assert tree[1] == ID_VALUE
    assert tree[2] == 2021


def test_parse_tree2():
    tree, idx = parse_tree(hex2bin("38006F45291200"), 0)
    print("38006F45291200", idx, tree)
    assert tree[0] == 1
    assert tree[1] == 6
    assert len(tree[2]) == 2
    b1, b2 = tree[2]
    # b1 is value 10
    assert b1[1] == 4
    assert b1[2] == 10
    # b2 is value 20
    assert b2[1] == 4
    assert b2[2] == 20


def test_parse_tree3():
    tree, idx = parse_tree(hex2bin("EE00D40C823060"), 0)
    print("EE00D40C823060", idx, tree)
    assert tree[0] == 7
    assert tree[1] == 3
    assert len(tree[2]) == 3
    b1, b2, b3 = tree[2]
    # b1 is value 1
    assert b1[1] == 4
    assert b1[2] == 1
    # b2 is value 2
    assert b2[1] == 4
    assert b2[2] == 2
    # b3 is value 3
    assert b3[1] == 4
    assert b3[2] == 3


def test_sum_versions():
    tree, idx = parse_tree(hex2bin("8A004A801A8002F478"), 0)
    assert sum_versions(tree) == 16

    tree, idx = parse_tree(hex2bin("620080001611562C8802118E34"), 0)
    assert sum_versions(tree) == 12

    tree, idx = parse_tree(hex2bin("C0015000016115A2E0802F182340"), 0)
    assert sum_versions(tree) == 23

    tree, idx = parse_tree(hex2bin("A0016C880162017C3686B18A3D4780"), 0)
    assert sum_versions(tree) == 31


def test_eval_tree():
    tree, idx = parse_tree(hex2bin("C200B40A82"), 0)
    assert eval_tree(tree) == 3

    tree, idx = parse_tree(hex2bin("04005AC33890"), 0)
    assert eval_tree(tree) == 54

    tree, idx = parse_tree(hex2bin("880086C3E88112"), 0)
    assert eval_tree(tree) == 7

    tree, idx = parse_tree(hex2bin("CE00C43D881120"), 0)
    assert eval_tree(tree) == 9

    tree, idx = parse_tree(hex2bin("D8005AC2A8F0"), 0)
    assert eval_tree(tree) == 1

    tree, idx = parse_tree(hex2bin("F600BC2D8F"), 0)
    assert eval_tree(tree) == 0

    tree, idx = parse_tree(hex2bin("9C005AC2F8F0"), 0)
    assert eval_tree(tree) == 0

    tree, idx = parse_tree(hex2bin("9C0141080250320F1802104A08"), 0)
    assert eval_tree(tree) == 1
