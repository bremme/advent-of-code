import argparse
import sys
from pathlib import Path
from types import SimpleNamespace

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
