from random import shuffle


class Node:
    def __init__(self, n):
        self.n = n
        self.left = None
        self.right = None


def parse(lines):
    x = [Node(int(x)) for x in lines]

    for i in range(len(x)):
        x[i].right = x[(i + 1) % len(x)]
        x[i].left = x[(i - 1) % len(x)]

    return x


def mix(x):

    m = len(x) - 1

    for k in x:
        if k.n == 0:
            z = k
            continue
        p = k
        if k.n > 0:
            for _ in range(k.n % m):
                p = p.right
            if k == p:
                continue
            k.right.left = k.left
            k.left.right = k.right
            p.right.left = k
            k.right = p.right
            p.right = k
            k.left = p
        else:
            for _ in range(-k.n % m):
                p = p.left
            if k == p:
                continue
            k.left.right = k.right
            k.right.left = k.left
            p.left.right = k
            k.left = p.left
            p.left = k
            k.right = p

    return z


def solve_part_one(lines: list[str], example: bool) -> int:
    x = parse(lines)
    z = mix(x)

    t = 0

    for _ in range(3):
        for _ in range(1000):
            z = z.right
        t += z.n

    return t


def solve_part_two(lines: list[str], example: bool) -> int:
    x = parse(lines)

    for k in x:
        k.n *= 811589153

    for _ in range(10):
        z = mix(x)

    t = 0

    for _ in range(3):
        for _ in range(1000):
            z = z.right
        t += z.n

    return t
