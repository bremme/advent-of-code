Run a single day
    run part one only
        run example data
        run real data
        run custom data
    run part two only
        run example data
        run real data
        run custom data
Run all days
Test after run

https://realpython.com/python-advent-of-code/


Coordinate systems

XY coordinates with y = down and x = right

RC coordiantes with row = right and column = down


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
* auto complete variants
* check invalid variant names
* list variants
* add day template
* add animations
* data download via cli
* answer upload via cli
* store answer when right

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