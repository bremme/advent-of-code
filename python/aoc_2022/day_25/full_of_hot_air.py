import math
from functools import cache


def parse(lines: list[str]):
    pass


lookup = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

reverse_lookup = {
    -2: "=",
    -1: "-",
    0: "0",
    1: "1",
    2: "2",
}


@cache
def snafu_to_decimal(snarfu: str):

    exponent = 0
    base = 5

    total = 0

    for char in reversed(snarfu):
        total += lookup[char] * base**exponent
        exponent += 1

    return total


def decimal_to_snafu(decimal: int) -> str:
    # 976 -> "2=-01"
    #                    total                   remainder
    #  2 * 625 = 1250  = 1250       1250 - 976 = 274
    # -2 * 125 = -250  = 1000       1000 - 976 =  24
    # -1 *  25 =  -25  =  975        975 - 976 =  -1
    #  0 *   5 =    0  =  975        975 - 976 =  -1
    #  1 *   1 =    1  =  976        976 - 976 =   0

    base = 5
    snarfu = ""
    total = 0

    # find largest exponent
    exponent = int(math.log(decimal) // math.log(base))

    while exponent >= 0:
        # find digit, which digit given the smallest remainder
        remainders = []
        for multiplier, symbol in reverse_lookup.items():
            value = multiplier * base**exponent
            new_total = total + value
            remainder = new_total - decimal
            remainders.append((abs(remainder), new_total, symbol))

        _, total, symbol = sorted(remainders)[0]
        snarfu += symbol
        exponent -= 1

    return snarfu


def solve_part_one(lines: list[str], example: bool) -> int:
    total = 0
    for line in lines:
        total += snafu_to_decimal(line)

    return decimal_to_snafu(total)


def solve_part_two(lines: list[str], example: bool) -> int:
    pass
