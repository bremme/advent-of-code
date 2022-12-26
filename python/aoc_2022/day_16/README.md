How to decide which valves to open which not? Its obivious that opening valves with a flow rate of 0 makes no sense.

should I first calculate how much pressure can be released by each valve


Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
        Valve CC has flow rate=2; tunnels lead to valves DD, BB
        Valve EE has flow rate=3; tunnels lead to valves FF, DD
    Valve II has flow rate=0; tunnels lead to valves AA, JJ
    Valve BB has flow rate=13; tunnels lead to valves CC, AA
        Valve JJ has flow rate=21; tunnel leads to valve II



Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG


Let investigate the example

AA
DD open     20
CC
BB open     13
AA
II
JJ open     21
II
AA
DD
EE
FF
GG
HH open     22
GG
EE open     3
DD
CC open     2

It looks like its some kind of comination between the length of the path towards a valve and the flow rate. Lets see if we can prove that.


determine distance for all valves

AA -> BB
AA -> CC
AA -> EE

etc.

https://www.youtube.com/watch?v=bLMj50cpOug

Floyd–Warshall algorithm solves all pairs shortest paths.
Breadth-first search is more efficient in this case



try to compress the network, valve with no flow_rate

https://www.codecademy.com/learn/nonlinear-data-structures-python/modules/trees-python/cheatsheet



# oxdf solutions

part one:  2,303 ms
part two: 62,649 ms

https://www.youtube.com/watch?v=rN4tVLnkgJU
https://gitlab.com/0xdf/aoc2022/-/tree/main/day16

# hyper-neutrino solutions

part one:    262 ms
part two: 21,751 ms

https://www.youtube.com/watch?v=bLMj50cpOug
https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day16p1.py
https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day16p2.py