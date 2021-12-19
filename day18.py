"""
Advent of Code 2021: day 18

Another challenging day, looks like I'm going to be parsing again.
That turned out to be easy, it was figuring out how to build the explode/split was the hard bit

I think is thinking in a functional/recursive manner which makes it harder.

Part B was thankfully very simple. It took ~10 seconds to compute, but thats not too slow.
"""
import pytest
from helper import *


def parse_line(s):
    tree, idx = parse_token(s, 0)
    return tree


def parse_token(s, idx):
    "parses the string from [index] returning the tree and new index"
    # should start with [
    if s[idx] != "[":
        return None, idx
    idx += 1
    if s[idx] != "[":
        # its a value
        left = int(s[idx])
        idx += 1
    else:
        # another token
        left, idx = parse_token(s, idx)
    # should be ,
    if s[idx] != ",":
        return None, idx
    idx += 1
    if s[idx] != "[":
        # its a value
        right = int(s[idx])
        idx += 1
    else:
        # another token
        right, idx = parse_token(s, idx)
    # should be ]
    if s[idx] != "]":
        return None, idx
    return [left, right], idx + 1


def add_to_leftmost(branch, val):
    """adds value to the leftmost part of the branch and returns the modified branch and 0.
    OR returns unchanged change and val if the val cannot be added"""
    if val == 0:
        return branch, val
    if type(branch) is int:
        return branch + val, 0
    # add to children, will do nothing is val become 0
    left, val = add_to_leftmost(branch[0], val)
    right, val = add_to_leftmost(branch[1], val)
    return [left, right], val


def add_to_rightmost(branch, val):
    if val == 0:
        return branch, val
    if type(branch) is int:
        return branch + val, 0
    # add to children, will do nothing is val become 0
    right, val = add_to_rightmost(branch[1], val)
    left, val = add_to_rightmost(branch[0], val)
    return [left, right], val


def explode(tree, depth=4):
    """explodes tree and returns new_tree,exploded_node"""
    if type(tree) is int:
        return tree, None
    if depth == 0:
        return 0, tree
    # see if left explodes
    left, ex = explode(tree[0], depth - 1)
    if ex is not None:
        # explosion, so attempt to apply to RHS
        right, ex_right = add_to_leftmost(tree[1], ex[1])
        return [left, right], [ex[0], ex_right]
    # see if right explodes
    right, ex = explode(tree[1], depth - 1)
    if ex is not None:
        # explosion, so attempt to apply to LHS
        left, ex_left = add_to_rightmost(tree[0], ex[0])
        return [left, right], [ex_left, ex[1]]
    return tree, None


def split(tree):
    """attempts to split, return tree,has_split
    where has_split is the flag if a split has occured
    """
    if type(tree) is int:
        if tree < 10:
            return tree, False
        left = tree // 2
        return [left, tree - left], True
    left, has_split = split(tree[0])
    if has_split:
        return [left, tree[1]], True
    right, has_split = split(tree[1])
    return [left, right], has_split


def add_pair(left, right):
    result = [left, right]
    while True:
        result, ex = explode(result)
        if ex is not None:
            continue
        result, has_split = split(result)
        if has_split == False:
            break
    return result


def add_list_pair(lines):
    result = parse_line(lines.pop(0))
    for l in lines:
        result = add_pair(result, parse_line(l))
    return result


def pair_magnitude(tree):
    if type(tree) is int:
        return tree
    return 3 * pair_magnitude(tree[0]) + 2 * pair_magnitude(tree[1])


def day18a(fname):
    return pair_magnitude(add_list_pair(load_strings(fname)))


def day18b(fname):
    nums = [parse_line(l) for l in load_strings(fname)]
    best = 0
    for i in nums:
        for j in nums:
            if i == j:
                continue
            res = add_pair(i, j)
            best = max(best, pair_magnitude(res))
    return best


################################################################
if __name__ == "__main__":
    print("day18a", day18a("input18.txt"))
    print("day18b", day18b("input18.txt"))

################################################################


def test_parse_line():
    assert parse_line("[1,2]") == [1, 2]
    assert parse_line("[[1,2],3]") == [[1, 2], 3]
    assert parse_line("[9,[8,7]]") == [9, [8, 7]]
    assert parse_line("[[1,9],[8,5]]") == [[1, 9], [8, 5]]
    assert parse_line("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]") == [
        [[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
        9,
    ]
    assert parse_line("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]") == [
        [[9, [3, 8]], [[0, 9], 6]],
        [[[3, 7], [4, 9]], 3],
    ]
    assert parse_line(
        "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"
    ) == [[[[1, 3], [5, 3]], [[1, 3], [8, 7]]], [[[4, 9], [6, 9]], [[8, 2], [7, 3]]]]


def test_explode_simple():
    # exploding a single item returns the item
    tree, remainder = explode([1, 1], 0)
    assert tree == 0
    assert remainder == [1, 1]


def test_explode_left():
    # pure left explosion
    tree, remainder = explode([[9, 8], 1], 1)
    print("test left", remainder, "tree", tree)
    assert tree == [0, 9]
    assert remainder == [9, 0]


def test_explode_right():
    # pure right explosion
    tree, remainder = explode([4, [3, 2]], 1)
    print("test right", remainder, "tree", tree)
    assert tree == [7, 0]
    assert remainder == [0, 2]


def test_explode():
    # cases from problem
    tree, remainder = explode([[[[[9, 8], 1], 2], 3], 4])
    print("case1", remainder, "tree", tree)
    assert tree == [[[[0, 9], 2], 3], 4]

    tree, remainder = explode([7, [6, [5, [4, [3, 2]]]]])
    print("case2", remainder, "tree", tree)
    assert tree == [7, [6, [5, [7, 0]]]]

    tree, remainder = explode([[6, [5, [4, [3, 2]]]], 1])
    assert tree == [[6, [5, [7, 0]]], 3]

    tree, remainder = explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    assert tree == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]

    tree, remainder = explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    assert tree == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]


def test_split():
    s, has_split = split(5)
    assert s == 5
    assert has_split == False

    s, has_split = split(10)
    assert s == [5, 5]
    assert has_split == True

    s, has_split = split([9, 9])
    assert s == [9, 9]
    assert has_split == False


def test_explode_split():
    left = [[[[4, 3], 4], 4], [7, [[8, 4], 9]]]
    right = [1, 1]
    tree = [left, right]
    print("after addition:", tree)
    assert tree == [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    tree, r = explode(tree)
    print("after explode:", tree)
    assert tree == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
    tree, r = explode(tree)
    print("after explode:", tree)
    assert tree == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
    # exploding should not do anything
    tree_copy, r = explode(tree)
    assert r is None
    assert tree_copy == tree
    # split
    tree, r = split(tree)
    print("after split:", tree)
    assert tree == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    tree, r = split(tree)
    print("after split:", tree)
    assert tree == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    tree, r = explode(tree)
    print("after explode:", tree)
    assert tree == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def test_add_pair():
    assert add_pair([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [
        [[[0, 7], 4], [[7, 8], [6, 0]]],
        [8, 1],
    ]


def test_add_list_pair():
    assert (
        add_list_pair(
            """[1,1]
    [2,2]
    [3,3]
    [4,4]""".split()
        )
        == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
    )

    assert (
        add_list_pair(
            """[1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]""".split()
        )
        == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
    )

    assert (
        add_list_pair(
            """[1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
    [6,6]""".split()
        )
        == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]
    )

    assert (
        add_list_pair(
            """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    [7,[5,[[3,8],[1,4]]]]
    [[2,[2,2]],[8,[8,1]]]
    [2,9]
    [1,[[[9,3],9],[[9,0],[0,7]]]]
    [[[5,[7,4]],7],1]
    [[[[4,2],2],6],[8,7]]""".split()
        )
        == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    )


def test_pair_magnitude():
    assert pair_magnitude([9, 1]) == 29
    assert pair_magnitude([1, 9]) == 21
    assert pair_magnitude([[9, 1], [1, 9]]) == 129
    assert pair_magnitude([[1, 2], [[3, 4], 5]]) == 143
    assert pair_magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
    assert pair_magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
    assert pair_magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
    assert pair_magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
    assert (
        pair_magnitude(
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
        )
        == 3488
    )


def test_day18a():
    assert day18a("test18.txt") == 4140


def test_day18b():
    assert day18b("test18.txt") == 3993
