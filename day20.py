"""
Advent of Code 2021: day 20

This looks like being a fun day, the infinite board is a little wrinkle.

We can probably get around this with a medium border.

A lot of testing done by eye with display() fn
but a test of result still added.

First attempt failed because of the algol:
0 items becomes a #, so we have an infinite # area
MAX items becomes a ., so second attempt converts back
BUT: edge cases leave me with an edging bit, so I fixed with a copy edge.

Part B might be a bit more tricky, as it needs 50 times.
Thats not so bad, but this might be super slow. Lets test
(test takes < 10 seconds)

"""
import pytest
from helper import *
import time


def parse_image(fname):
    "scans fname an returns (algol,image), where image is an array of strings"
    algol = None
    image = []
    for l in load_strings(fname):
        if algol is None:
            algol = l
            continue
        if len(l) == 0:
            continue
        image.append(l)

    return algol, image


def print_image(image):
    for i in image:
        print(i)


def add_border(image, sz):
    "returns new image with sz empty spaces on edges"
    h, w = len(image), len(image[0])
    blank = "." * (w + sz + sz)
    edge = "." * sz
    result = []
    for i in range(sz):
        result.append(blank)
    for line in image:
        result.append(edge + line + edge)
    for i in range(sz):
        result.append(blank)
    return result


def enhance_image(algol, image):
    "enhances image"
    # the algol only works on 1..w-1 so we need to add a boarder as we go
    h, w = len(image), len(image[0])
    result = []
    for y in range(1, h - 1):
        line = ""
        for x in range(1, w - 1):
            # count '#' in 3x3 grid'
            digits = ""
            for j in range(y - 1, y + 2):
                digits += image[j][x - 1 : x + 2]
            # change . to 0 & # to 1 then convert to int
            digits = digits.replace(".", "0").replace("#", "1")
            val = int(digits, 2)
            # lookup in algol
            line += algol[val]
        # add copies to either end of line
        result.append(line[0] + line + line[-1])
    # add copies top & bottom
    result = [result[0]] + result + [result[-1]]
    return result


def day20a(fname):
    algol, image = parse_image(fname)
    image = add_border(image, 5)
    image = enhance_image(algol, image)
    image = enhance_image(algol, image)
    # count #'s
    return sum((l.count("#") for l in image))


def day20b(fname):
    algol, image = parse_image(fname)
    # each step seems to increase size by 1 so, 50 steps will expand 50
    # add 60 to be sure
    image = add_border(image, 60)
    for i in range(50):
        image = enhance_image(algol, image)
    # count #'s
    return sum((l.count("#") for l in image))


def display(fname):
    border = 60
    iteration = 50
    algol, image = parse_image(fname)
    print("algol", algol)
    print("raw image")
    print_image(image)
    image = add_border(image, border)
    print("padded image")
    print_image(image)
    for i in range(iteration):
        image = enhance_image(algol, image)
        if i % 10 == 0:
            print("enchanced image", 0)
            print_image(image)

    print("cells", sum((l.count("#") for l in image)))


################################################################
if __name__ == "__main__":
    start = time.perf_counter()
    ##    display("test20.txt")
    ##    display("input20.txt")
    ##    print("day20a", day20a("input20.txt"))
    print("day20b", day20b("input20.txt"))

    print("time taken", time.perf_counter() - start)

################################################################


def test_parse_image():
    algol, image = parse_image("test20.txt")
    assert len(algol) == 512
    assert len(image) == 5
    assert len(image[0]) == 5


def test_day20a():
    assert day20a("test20.txt") == 35


def test_day20b():
    assert day20b("test20.txt") == 3351
