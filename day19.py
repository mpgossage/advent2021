"""
Advent of Code 2021: day 19

This looks like being a near nightmare day.  Its asking to build a SLAM algorithm.

I have a very rough idea one how to approach this.

Found that the algol will not match input19.txt with criteria or 12 overlaps,
so dropped threshold to 10

Again part B is easy
"""
import pytest
from helper import *

MAX_ROTATIONS = 24  # max values for rotate_delta
MATCH_CRITERIA = 10


def parse_scanners(fname):
    scanners = []
    beacons = []
    for l in load_strings(fname):
        if len(l) == 0:
            continue
        if l[:3] == "---":
            # scanner boundary
            if len(beacons) > 0:
                scanners.append(beacons)
            beacons = []
            continue
        beacons.append(tuple((int(t) for t in l.split(","))))

    if len(beacons) > 0:
        scanners.append(beacons)
    return scanners


def get_beacon_deltas(scanner):
    """A scanners has many beacons, returns {(dx,dy,dz)=>(i1,i2)}
    where dx,dy,dz is the delta distance between 2 beacons & i1,i2 are the indexes"""
    deltas = {}
    ln = len(scanner)
    for i in range(ln):
        for j in range(i + 1, ln):
            dx = scanner[i][0] - scanner[j][0]
            dy = scanner[i][1] - scanner[j][1]
            dz = scanner[i][2] - scanner[j][2]

            deltas[(dx, dy, dz)] = (i, j)
    return deltas


def rotate_delta(delta, index):
    """there are 24 rotational version, up,down,left,right,forward,back * 4 spins. This is a quick lookup"
    used: https://danceswithcode.net/engineeringnotes/rotations_in_3d/demo3D/rotations_in_3d_tool.html
    to calculate them"""
    dx, dy, dz = delta
    if index == 0:
        return delta
    elif index == 1:
        return dx, -dz, dy
    elif index == 2:
        return dx, -dy, -dz
    elif index == 3:
        return dx, dz, -dy
    elif index == 4:
        return -dy, dx, dz
    elif index == 5:
        return dz, dx, dy
    elif index == 6:
        return dy, dx, -dz
    elif index == 7:
        return -dz, dx, -dy
    elif index == 8:
        return -dx, -dy, dz
    elif index == 9:
        return -dx, dz, dy
    elif index == 10:
        return -dx, dy, -dz
    elif index == 11:
        return -dx, -dz, -dy
    elif index == 12:
        return dy, -dx, dz
    elif index == 13:
        return -dz, -dx, dy
    elif index == 14:
        return -dy, -dx, -dz
    elif index == 15:
        return dz, -dx, -dy
    elif index == 16:
        return dz, dy, -dx
    elif index == 17:
        return dy, -dz, -dx
    elif index == 18:
        return -dz, -dy, -dx
    elif index == 19:
        return -dy, dz, -dx
    elif index == 20:
        return -dz, dy, dx
    elif index == 21:
        return -dy, -dz, dx
    elif index == 22:
        return dz, -dy, dx
    else:
        return dy, dz, dx


def match_beacons(known_beacons, test_beacons):
    "attempts to match test_beacons to know_beacons, returns ((dx,dy,dz),rotation) of test or None"
    known_deltas = get_beacon_deltas(known_beacons)
    test_deltas = get_beacon_deltas(test_beacons)
    for i in range(MAX_ROTATIONS):
        pos = []
        b_matched = set()
        for delta in test_deltas:
            rdelta = rotate_delta(delta, i)
            if rdelta in known_deltas:
                # A=>B in known space matches points P=>Q in rotated space
                a, b = known_deltas[rdelta]
                pos_a, pos_b = known_beacons[a], known_beacons[b]
                p, q = test_deltas[delta]
                rpos_p, rpos_q = rotate_delta(test_beacons[p], i), rotate_delta(
                    test_beacons[q], i
                )
                # estimated position Z = OA-ZP or OB-ZQ
                z1 = (pos_a[0] - rpos_p[0], pos_a[1] - rpos_p[1], pos_a[2] - rpos_p[2])
                z2 = (pos_b[0] - rpos_q[0], pos_b[1] - rpos_q[1], pos_b[2] - rpos_q[2])
                if z1 == z2:
                    pos.append(z1)
                # note: which beacons matched
                b_matched.add(a)
                b_matched.add(b)
        if len(b_matched) >= MATCH_CRITERIA:
            # match, double check: if the pos is consistent
            for p in pos:
                if p != pos[0]:
                    print("warning, pos disagreement", pos[0], p)
            return pos[0], i
    ##        elif len(b_matched)>=4:
    ##            print(f"close match {len(b_matched)}")
    return None


def transform_beacons(beacons, pos, rot):
    "rotates and moves beacons and returns the new beacon positions"

    def trans(p, pos, rot):
        t = rotate_delta(p, rot)
        return (pos[0] + t[0], pos[1] + t[1], pos[2] + t[2])

    return [trans(p, pos, rot) for p in beacons]


def match_all_beacons(beacons):
    "matches all beacons together, returns [transformed_beacons],[locations]"
    ln = len(beacons)
    # known[i] is None if not matched, or transformed beacon locations
    known = [None] * ln
    locs = [None] * ln
    # known[0] is known, as its the zero position
    known[0] = beacons[0]
    locs[0] = (0, 0, 0)

    found = True
    while found:
        found = False
        for k in range(ln):
            for u in range(ln):
                # k is a known beacon, u is unknown beacon
                if (known[k] is not None and known[u] is None) == False:
                    continue
                # attempt to match them
                result = match_beacons(known[k], beacons[u])
                if result is None:
                    continue
                pos, rot = result
                print(f"match_beacons {k} {u} with {pos} {rot}")
                # transform beacons[u] with transformed version
                known[u] = transform_beacons(beacons[u], pos, rot)
                locs[u] = pos
                found = True
        num_found = sum(1 for k in known if k is not None)
        print(f"cycle ended, found {num_found}/{len(known)}")
    return known, locs


def count_unique_beacons(scanners):
    allb = set()
    for s in scanners:
        for b in s:
            allb.add(b)
    return len(allb)


def day19a(fname):
    scanners = parse_scanners(fname)
    scanners, locs = match_all_beacons(scanners)
    return count_unique_beacons(scanners)


def day19b(fname):
    scanners = parse_scanners(fname)
    scanners, locs = match_all_beacons(scanners)
    best = 0
    for x1, y1, z1 in locs:
        for x2, y2, z2 in locs:
            dist = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
            best = max(best, dist)
    return best


################################################################
if __name__ == "__main__":
    print("day19a", day19a("input19.txt"))
    print("day19b", day19b("input19.txt"))

################################################################


def test_parse_scanners():
    scanners = parse_scanners("test19.txt")
    assert len(scanners) == 5
    assert len(scanners[0]) == 25
    assert scanners[0][0] == (404, -588, -901)
    assert scanners[0][24] == (459, -707, 401)


def test_get_beacon_deltas():
    scanners = parse_scanners("test19.txt")
    deltas = get_beacon_deltas(scanners[0])
    assert len(deltas) == 25 * 24 // 2
    # not bothering to check exact values


def test_match_beacons():
    scanners = parse_scanners("test19.txt")
    scan0, scan1 = scanners[0], scanners[1]
    pos1, rot1 = match_beacons(scan0, scan1)
    assert pos1 == (68, -1246, -43)
    # assumption: we know the pos & rotation of point 1
    # so if we rotate+translate the points, we should see a 1:1 match for 12 of the points
    scan1 = transform_beacons(scan1, pos1, rot1)

    count = 0
    for tp in scan1:
        if tp in scan0:
            count += 1
    assert count >= 12

    # scan4 should overlap scan1, we will used the transformed version
    scan4 = scanners[4]
    pos4, rot4 = match_beacons(scan1, scan4)
    assert pos4 == (-20, -1133, 1061)
    scan4 = transform_beacons(scan4, pos4, rot4)

    scan2, scan3 = scanners[2], scanners[3]
    # guessing 2 matches 4
    pos2, rot2 = match_beacons(scan4, scan2)
    assert pos2 == (1105, -1205, 1229)
    scan2 = transform_beacons(scan2, pos2, rot2)

    # guessing 3 matches 1
    pos3, rot3 = match_beacons(scan1, scan3)
    assert pos3 == (-92, -2380, -20)


def test_match_all():
    scanners = parse_scanners("test19.txt")
    scanners, locs = match_all_beacons(scanners)
    print(scanners)
    # total unique beacons should be 79
    assert count_unique_beacons(scanners) == 79


def test_day19a():
    assert day19a("test19.txt") == 79


def test_day19b():
    assert day19b("test19.txt") == 3621
