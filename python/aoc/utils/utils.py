import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

DATA_DIRECTORY = Path(__file__).parent.parent.parent.parent / "data"


@dataclass
class PuzzleAnswers:
    part: int
    example: bool
    value: int


@dataclass
class PuzzleAnswerCollection:
    answers: list[PuzzleAnswers]

    def get_puzzle_answer(self, part, example):
        for answer in self.answers:
            if answer.part == part and answer.example == example:
                return answer
        raise ValueError("No answer for ")


def read_puzzle_input(day: int, year: int, example: bool) -> list[str]:
    input_file = (
        DATA_DIRECTORY
        / f"{year}"
        / f"day_{day}"
        / f"puzzle_input{'_example' if example else ''}.txt"
    )
    return read_puzzle_input_file(input_file)


def read_puzzle_input_file(input_file) -> list[str]:
    with open(input_file, "r", encoding="utf-8") as fh:
        return [line for line in fh.read().splitlines()]


def read_puzzle_answer_file(day: int, year: int, part: int, example: bool):
    answer_file = (
        DATA_DIRECTORY
        / f"{year}"
        / f"day_{day}"
        / f"puzzle_answer{'_example' if example else ''}.json"
    )

    with open(answer_file, "r") as fh:
        data = json.load(fh)

    return data


def read_puzzle_answer(day: int, year: int, part: int, example: bool):
    parts = {1: "one", 2: "two"}

    data = read_puzzle_answer_file(day, year, part, example)

    return data[f"part_{parts[part]}"]


def store_puzzle_answer(
    day: int, year: int, part: int, example: bool, answer: Union[int, str]
):
    answer_file = (
        DATA_DIRECTORY
        / f"{year}"
        / f"day_{day}"
        / f"puzzle_answer{'_example' if example else ''}.json"
    )
    parts = {1: "one", 2: "two"}

    if answer_file.is_file():
        with open(answer_file, "r") as fh:
            data = json.load(fh)
    else:
        data = {"part_one": None, "part_two": None}

    data[f"part_{parts[part]}"] = answer

    with open(answer_file, "w") as fh:
        json.dump(data, fh, indent=4)


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


def pairs(items, overlapping=False):
    # loop with 2 items at a time (one pair)
    for index in range(0, len(items) - 1, 2):
        yield items[index], items[index + 1]


def pairs_overlapping(items):
    # loop with 2 items at a time (one pair)
    for index in range(0, len(items) - 1, 1):
        yield items[index], items[index + 1]


def pairs_flipped(items):
    # loop with 2 items at a time (one pair)
    for index in range(0, len(items) - 1, 2):
        yield items[index + 1], items[index]


def pairs_flipped_overlapping(items):
    # loop with 2 items at a time (one pair)
    for index in range(0, len(items) - 1, 1):
        yield items[index + 1], items[index]


def double_pairs(items):
    # loop with 4 items, two pairs at a time
    for i in range(0, len(items) - 3, 4):
        first = items[i], items[i + 1]
        second = items[i + 2], items[i + 3]
        yield first, second


def double_pairs_flipped(items):
    # loop with 4 items, two pairs at a time
    for i in range(0, len(items) - 3, 4):
        first = items[i + 1], items[i]
        second = items[i + 3], items[i + 2]
        yield first, second


def double_pairs_overlapping(items):
    # loop with 4 items, two pairs at a time
    for i in range(0, len(items) - 3, 2):
        first = items[i], items[i + 1]
        second = items[i + 2], items[i + 3]
        yield first, second


def double_pairs_flipped_overlapping(items):
    # loop with 4 items, two pairs at a time
    for i in range(0, len(items) - 3, 2):
        first = items[i + 1], items[i]
        second = items[i + 3], items[i + 2]
        yield first, second
