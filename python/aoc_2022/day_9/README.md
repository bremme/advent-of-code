head and tail start at same position overlapping
tail need to always touch the head (diagonal counts as well)

probably start is in bottom left?


. . . .
. . . .
. . . .
. . H .
. T . .

. . . .
. . . .
. . H .
. . . .
. T . .

. . . .
. . . .
. . . .
. . . H
. T . .


0:  no move needed
1:  one horizontal or vertical move needed
D:  1 diagonal move needed

. . . . . . .
. D 1 1 1 D .
. 1 0 0 0 1 .
. 1 0 H 0 1 .
. 1 0 0 0 1 .
. D 1 1 1 D .
. . . . . . .

0: vertical <= 1 and horizontal <= 1
1: vertical <= 2 and horizontal <= 1 or vertical <= 1 and horizontal <= 2
D: vertical <= 2 and horizontal <= 2

. . . . . . .
.SE S S S SW.
. E 0 0 0 W .
. E 0 H 0 W .
. E 0 0 0 W .
.NE N N N NW.
. . . . . . .

......
......
......
....H.
s..T..

......
......
....H.
......
s..T..

......
......
....H.
....T.
s.....

0:  abs(horizontal) <=  1 and abs(vertical) <= 1
W:      horizontal  ==  2 and abs(vertical) <= 1
E:      horizontal  == -2 and abs(vertical) <= 1
N  abs(horizontal)  <=  1 and vertical == -2
S: abs(horizontal)  <=  1 and vertical == 2

SW: horizontal ==  2 and vertical ==  2
NW: horizontal ==  2 and vertical == -2
NE: horizontal == -2 and vertical == -2
SE: horizontal == -2 and vertical ==  2

. . . .  4 . . . . . .
. . H .  3 . . . . . .
. . . .  2 . . . . . .
. . H .  1 . . . . . .
. . . T  . . . . . . .
. . . . -1 . . . . . .
. . . . -2 . . . . . .
. . . . -3 . . . . . .
. . . . -4 . . . . . .
4-3-2-1  0 1 2 3 4 5 6

U 4
moved head from (4, 0) to (4, 1) with move U
moved tail from (3, 0) to (3, 0) with move -
moved head from (4, 1) to (4, 2) with move U
moved tail from (3, 0) to (3, 1) with move N -> NE??

head (4, 2) tail 3, 0)


. .  . . .  . .
. . SE S SW . .
. SE 0 0 0  SW.
. E  0 H 0  W .
. NE 0 0 0  NW.
. . NE N NW . .
. .  . . .  . .


# example

== E 4 ==
moved head from (0, 0) to (1, 0) with move E (0)
moved tail from (0, 0) to (0, 0) with move 0
moved head from (1, 0) to (2, 0) with move E (1)
moved tail from (0, 0) to (1, 0) with move E
moved head from (2, 0) to (3, 0) with move E (2)
moved tail from (1, 0) to (2, 0) with move E
moved head from (3, 0) to (4, 0) with move E (3)
moved tail from (2, 0) to (3, 0) with move E
== N 4 ==
moved head from (4, 0) to (4, 1) with move N (4)
moved tail from (3, 0) to (3, 0) with move 0
moved head from (4, 1) to (4, 2) with move N (5)
moved tail from (3, 0) to (4, -1) with move SE      -> NE
moved head from (4, 2) to (4, 3) with move N (6)
moved tail from (4, -1) to (4, -1) with move 0
moved head from (4, 3) to (4, 4) with move N (7)
moved tail from (4, -1) to (4, -1) with move 0