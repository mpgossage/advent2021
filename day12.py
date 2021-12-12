"""
Advent of Code 2021: day 12
Its graph theory day.

Going to model my graph as a map{node=>[other nodes]} which is symetrical.
Spotted one possible infinte loop condition if two large caves are linked.
Then it would be legal to A,B,A,B,A,...
Assuming it doesn't happen first and will add extra check if needed.

Part B requres a rebuild of rules for find_all_routes() so I will need to rethink that.

Overall Part B caused a few issues, and a few infinite loops, but nothing too serious
"""
import pytest
from helper import *


def lines_to_graph(fname):
    graph = {}
    for l in load_strings(fname):
        a, b = l.split("-")
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        graph[b].append(a)
    return graph


def is_small(s):
    "if a cave is small"
    # assuming start & end are small, so we will not visit many times
    return s.islower()


def find_all_routes(graph):
    """returns all paths through the map
    returns a list of paths where a path is a list of locations"""
    # using BFS as it gets all. Its slow, but for a few K, thats acceptable
    routes = []
    # todo is the list of paths, the last item is current location
    todo = [["start"]]
    while todo:
        path = todo.pop()
        loc = path[-1]
        exits = graph[loc]
        for e in exits:
            # finished
            if e == "end":
                routes.append(path + [e])
                continue
            # cannot visit small twice
            if is_small(e) and e in path:
                continue
            # add to list
            todo.append(path + [e])
    return routes


def day12a(fname):
    g = lines_to_graph(fname)
    r = find_all_routes(g)
    return len(r)


def find_all_routes2(graph):
    """Alternate version which allows visiting a single small creturns all paths through the map
    returns a list of paths where a path is a list of locations"""
    # using BFS as it gets all. Its slow, but for a few K, thats acceptable
    routes = []
    # todo is the list of paths
    # where a path is ([L1,L2,L3],A)
    # where L1... is the path & A is if we have visited a small cave twice
    todo = [(["start"], False)]
    while todo:
        t = todo.pop()
        path, visited_small = t

        loc = path[-1]
        exits = graph[loc]
        for e in exits:
            # finished
            if e == "end":
                routes.append(path + [e])
                continue
            # cannot visit start again
            if e == "start":
                continue
            # can only visit a single small cave once
            if is_small(e) and e in path:
                if visited_small == True:
                    # already visited before, don't try again
                    continue
                else:
                    # allow this time only
                    todo.append((path + [e], True))
                    continue
            # add to list
            todo.append((path + [e], visited_small))

    return routes


def day12b(fname):
    "no test for this, as all tests checked find_all_routes() instead"
    g = lines_to_graph(fname)
    r = find_all_routes2(g)
    return len(r)


################################################################
if __name__ == "__main__":
    print("day12a", day12a("input12.txt"))
    print("day12b", day12b("input12.txt"))

################################################################


def test_lines_to_graph():
    g = lines_to_graph("test12a.txt")
    assert sorted(g["start"]) == ["A", "b"]
    assert sorted(g["A"]) == ["b", "c", "end", "start"]


def test_find_all_routes():
    g = lines_to_graph("test12a.txt")
    r = find_all_routes(g)
    print(r)
    assert len(r) == 10


def test_day12a():
    assert day12a("test12a.txt") == 10
    assert day12a("test12b.txt") == 19
    assert day12a("test12c.txt") == 226


def test_day12b():
    assert day12b("test12a.txt") == 36
    assert day12b("test12b.txt") == 103
    assert day12b("test12c.txt") == 3509
