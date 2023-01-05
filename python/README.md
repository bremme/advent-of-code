# Installation

pip install -e .

# Usage

aoc --help

aoc run --day 17 --part 2 --example --assert

# TODO

Overall goals

* learn some new things
* use names from the problem description
* should be readable code
* use abstractions to improve readability
* but maintain a reasonable amount of performance
* ideally every day should run under 1s
* make it clear which algorithm / strategy is used under the hood
* add tests
* add cli tool to make it easy to run
* type hinting
* github badgest
* github actions
* answer looks like answer in description


# TODO

* aoc cli
    * run sub commands
        * auto complete variants
        * run all days
        * upload answer
        * save answer (when correct)
        * debug add breakpoint with line number
    * list sub command
        * variants
    * generate sub command
        *  day(s) stubs
    * download
        * download data
* add animations
* data download via cli
* answer upload via cli
* store answer when right
* improve logging
    * add extra level
    * dynamicly change level based on example or not
* utilities
    * for several coordinate systems (row, column vs x, y etc.)
    * remove duplication form days


# General things I've learnerd

Breadth-first search (BFS):
https://en.wikipedia.org/wiki/Breadth-first_search

Depth-first search (DFS)
https://en.wikipedia.org/wiki/Depth-first_search


https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/

BFS uses a queue with first in first out. slower?
vertex bases technique

DFS uses a stack
edge based technique

* DFS
    * day 16: Probascidea Volcanium
    * day 19: Not Enough Minerals
    * day 24: Blizzward Basin

* Double linked list
    * day 20: Grove Positioning System

* Dijkstra
    * day 12: Hill Climbing Algorithm
    * day 24: Blizzward Basin

* Binairy search
    * day 21: Monkey Math

Optimizations by finding patterns in day 17 for example.