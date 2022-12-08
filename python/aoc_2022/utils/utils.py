import sys
from pathlib import Path
from types import SimpleNamespace

DATA_DIRECTORY = Path(__file__).parent.parent.parent / "data"


def read_puzzle_input(day: int, example: bool):
    input_file = (
        DATA_DIRECTORY / f"day_{day}_puzzle_input{'_example' if example else ''}.txt"
    )
    return read_puzzle_input_file(input_file)


def read_puzzle_input_file(input_file) -> tuple[str]:
    with open(input_file, "r", encoding="utf-8") as fh:
        return [line for line in fh.read().splitlines()]


def parse_args():
    input_file = sys.argv[1]
    return SimpleNamespace(input_file=input_file)
