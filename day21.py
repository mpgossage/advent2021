"""
Advent of Code 2021: day 21

This looks like a great time to play with generators.
It looks simple enough (at least for now)

Part B is a monster, quantum die here we come, infinite possiblities
"""
import pytest
from helper import *


def load_game(fname):
    "return (start1,start2)"
    return [int(l.split(':')[1]) for l in load_strings(fname)]

def deterministic_dice():
    while True:
        for i in range(1,101):
            yield i

def take_turn(pos,dice):
    roll = next(dice)+next(dice)+next(dice)
    pos+=roll
    pos%=10
    if pos==0: pos=10
    return pos

def play_game(p1,p2,dice):
    s1,s2=0,0
    WIN=1000
    rolls=0
    while True:
        p1=take_turn(p1,dice)
        s1+=p1
        rolls+=3
        if s1>=WIN: break
        p2=take_turn(p2,dice)
        s2+=p2
        rolls+=3
        if s2>=WIN: break
    return s1,s2,rolls

def day21a(fname):
    p1,p2=load_game(fname)
    dice = deterministic_dice()
    s1,s2,rolls=play_game(p1,p2,dice)
    return min(s1,s2)*rolls

"""
To solve quantum states we have a dict of states:
{(p1,p2,s1,s2):occurences}

for example: if there is only once state
{(1,1,0,0):1}
there are 27 different rolls for 3 dice, but not all unique.

3 is only possible one way (1,1,1)
4 has 3 ways (1,1,2),(1,2,1),(2,1,1)
5 has 6 ways (1,1,3),(1,3,1),(3,1,1),(1,2,2),(2,1,2),(2,2,1)
6 has 7 ways (1,2,3),(1,3,2),(2,3,1),(2,1,3),(3,1,2),(3,2,1),(2,2,2)
7 has 6 ways (2,2,3),(2,3,2),(3,2,2),(1,3,3),(3,1,3),(3,3,1)
8 has 3 ways (2,3,3),(3,2,3),(3,3,2)
9 has 1 way (3,3,3)

So p1 who is on square 1 can be at:
4:1, 5:3, 6:6, 7:7, 8:6, 9:3, 10:1
so we can represent this as a set of states, instead of all 27 versions

"""
QUANTUM={3:1,4:3,5:6,6:7,7:6,8:3,9:1}
QWIN=21

def move(p,s,m):
    p=(p+m)%10
    if p==0: p==10
    return p,p+s

def take_qturn(states,is_p1_turn):
    result={}
    for state,val in states.items():
        p1,p2,s1,s2 = state
        for quantum_roll,quantum_val in QUANTUM.items():
            if is_p1_turn:
                np,ns=move(p1,s1,quantum_roll)
                new_state=(np,p2,ns,s2)
            else:
                np,ns=move(p2,s2,quantum_roll)
                new_state=(p1,np,s1,ns)        
            if new_state not in result: result[new_state]=0
            result[new_state]+=quantum_val*val
    return result

def filter_qwinners(states):
    "returns (num_p1_win,num_p2_win,non_win_states)"
    non_win={}
    p1_win,p2_win = 0,0
    for state,val in states.items():
        p1,p2,s1,s2 = state
        if s1>=QWIN:
            p1_win+=val
        elif s2>=QWIN:
            p2_win+=val
        else:
            non_win[state]=val
    return p1_win,p2_win,non_win
        
def play_qgame(p1,p2):
    p1win,p2win=0,0
    states={(p1,p2,0,0):1}
    while states:
        p1w,p2w,states = filter_qwinners(take_qturn(states,True))
        print("p1",p1w,states)
        p1win+=p1w
        p2win+=p2w
        p1w,p2w,states = filter_qwinners(take_qturn(states,False))
        print("p2",p2w,states)
        p1win+=p1w
        p2win+=p2w
    return p1win,p2win




################################################################
if __name__ == "__main__":
    print("day21a", day21a("input21.txt"))
##    print("day01b", day01b("input01.txt"))

################################################################


def test_load_game():
    assert load_game("test21.txt") == [4,8]

def test_take_turn():
    p1,p2=4,8
    dice = deterministic_dice()
    p1=take_turn(p1,dice)
    assert p1 ==10
    p2=take_turn(p2,dice)
    assert p2 ==3
    p1=take_turn(p1,dice)
    assert p1 ==4
    p2=take_turn(p2,dice)
    assert p2 ==6
    p1=take_turn(p1,dice)
    assert p1 ==6
    p2=take_turn(p2,dice)
    assert p2 ==7
    p1=take_turn(p1,dice)
    assert p1 ==6
    p2=take_turn(p2,dice)
    assert p2 ==6

def test_day21a():
    assert day21a("test21.txt")==739785

def test_quantum():
    states={(4,8,0,0):1}
    print("states 0",states)
    states=take_qturn(states,True)
    print("states p1",states)
    assert sum(states.values()) == 27
    states=take_qturn(states,False)
    print("states p2",states)
    assert sum(states.values()) == 27*27
    states=take_qturn(states,True)
    print("states p1",states)
    assert sum(states.values()) == 27**3
    states=take_qturn(states,False)
    print("states p2",states)
    assert sum(states.values()) == 27**4
    states=take_qturn(states,True)
    print("states p1",states)
    assert sum(states.values()) == 27**5
    states=take_qturn(states,False)
    print("states p2",states)
    assert sum(states.values()) == 27**6
    
    p1win,p2win=play_qgame(4,8)
    print("p1",p1win,"p2",p2win)
    assert False


