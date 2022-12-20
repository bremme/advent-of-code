import argparse
import re
from pathlib import Path

DATA_DIRECTORY = Path(__file__).parent.parent.parent.parent / "data"


def read_puzzle_input(day: int, example: bool) -> list[str]:
    input_file = (
        DATA_DIRECTORY / f"day_{day}_puzzle_input{'_example' if example else ''}.txt"
    )
    return read_puzzle_input_file(input_file)


def read_puzzle_input_file(input_file) -> list[str]:
    with open(input_file, "r", encoding="utf-8") as fh:
        return [line for line in fh.read().splitlines()]


def parse_args():
    parser = argparse.ArgumentParser(prog="Advent of Code")
    parser.add_argument("-f", "--file", dest="input_file")
    parser.add_argument("-p", "--part")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    return args


def parse_positive_integers(line: str):
    return list(map(int, re.findall(r"\d+", line)))


def parse_integers(line: str):
    return list(map(int, re.findall(r"-?\d+", line)))


def parse_floats(line: str):
    return list(map(float, re.findall(r"-?\d+\.?\d*", line)))


# loop functions


def pairs(items):
    # loop with 2 items at a time (one pair)
    for index in range(0, len(items) - 1, 2):
        yield items[index], items[index + 1]


def pairs_flipped(items):
    # loop with 2 items at a time (one pair)
    for index in range(0, len(items) - 1, 2):
        yield items[index + 1], items[index]


def double_pairs(items):
    # loop with 4 items, two pais at a time
    for i in range(0, len(items) - 2, 4):
        first = items[i], items[i + 1]
        second = items[i + 2], items[i + 3]
        yield first, second


def double_pairs_flipped(items):
    # loop with 4 items, two pais at a time
    for i in range(0, len(items) - 2, 4):
        first = items[i + 1], items[i]
        second = items[i + 3], items[i + 2]
        yield first, second


def double_pairs_overlapping(items):
    # loop with 4 items, two pais at a time
    for i in range(0, len(items) - 2, 2):
        first = items[i], items[i + 1]
        second = items[i + 2], items[i + 3]
        yield first, second


def double_pairs_flipped_overlapping(items):
    # loop with 4 items, two pais at a time
    for i in range(0, len(items) - 2, 2):
        first = items[i + 1], items[i]
        second = items[i + 3], items[i + 2]
        yield first, second
