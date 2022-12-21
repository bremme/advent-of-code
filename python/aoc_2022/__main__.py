import argparse
import cProfile
import io
import logging
import pstats
import time
from pathlib import Path
from typing import Optional

from aoc_2022.app.puzzle_finder import Puzzle, PuzzleFinder
from aoc_2022.utils import utils
from aoc_2022.utils.utils import read_puzzle_input, read_puzzle_input_file
from ipdb import launch_ipdb_on_exception

logger = logging.getLogger()


def _parse_args():
    parser = argparse.ArgumentParser(prog="Advent of Code")

    parser.add_argument("-d", "--day", type=int, required=True)
    parser.add_argument("-p", "--part", type=int)
    parser.add_argument("--variant", default="default")
    parser.add_argument("-e", "--example", action="store_true")

    parser.add_argument("-f", "--file", type=str, dest="input_file")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--assert", action="store_true")

    return parser.parse_args()


def _setup_logger(verbose):
    # setup logger
    FORMAT = "%(message)s"
    logging.basicConfig(format=FORMAT)

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def _solve_puzzles(
    puzzle: Puzzle, variant: str, part: Optional[int], lines: list[str], example: bool
):
    assert_answer = False
    solution = puzzle.get_solution(variant)

    logger.info(f"---- Day {puzzle.day}: {puzzle.title} ---")

    if part in [1, None]:
        logger.info(f"--- Part One {'Example' if example else ''}---")
        start = time.time()
        answer_part_one = solution.module.solve_part_one(lines, example)
        duration_ms = (time.time() - start) * 1_000
        logger.info(f"Answer part one: {answer_part_one}\t(took {duration_ms:,.3f} ms)")

        if assert_answer:
            expected_answer = utils.read_puzzle_answer(
                day=puzzle.day, year=2022, part=1, example=example
            )

            if answer_part_one != expected_answer:
                raise AssertionError(f"{answer_part_one} != {expected_answer}")

            logger.info(
                f"Assertion of answer was successfull ({answer_part_one} == {expected_answer})"
            )

    if part in [2, None]:
        logger.info(f"--- Part Two {'Example' if example else ''}---")
        start = time.time()
        answer_part_two = solution.module.solve_part_two(lines, example)
        duration_ms = (time.time() - start) * 1_000
        logger.info(f"Answer part two: {answer_part_two}\t(took {duration_ms:,.3f} ms)")

        if assert_answer:
            expected_answer = utils.read_puzzle_answer(
                day=puzzle.day, year=2022, part=2, example=example
            )

            if answer_part_two != expected_answer:
                raise AssertionError(f"{answer_part_one} != {expected_answer}")

            logger.info(
                f"Assertion of answer was successfull ({answer_part_two} == {expected_answer})"
            )


class profile:
    def __init__(self, sortby="totime", amount=1.0) -> None:
        self.sortby = sortby
        self.amount = amount
        self.profile = cProfile.Profile()

    def __enter__(self):
        self.profile.enable()
        return self.profile

    def __exit__(self, type, value, traceback):
        self.profile.disable()
        stream = io.StringIO()

        stats = (
            pstats.Stats(self.profile, stream=stream)
            .sort_stats(self.sortby)
            .print_stats(self.amount)
        )
        print(stream.getvalue())


def main():
    PACKAGE_ROOT = Path(__file__).parent

    puzzles = PuzzleFinder.find_puzzles(PACKAGE_ROOT)

    args = _parse_args()

    _setup_logger(args.verbose)

    # read input data
    if args.input_file:
        lines = read_puzzle_input_file(args.input_file)
    else:
        lines = read_puzzle_input(args.day, 2022, args.example)

    puzzle = puzzles.get_puzzle(args.day)

    solve_puzzle_args = {
        "puzzle": puzzle,
        "variant": args.variant,
        "part": args.part,
        "lines": lines,
        "example": args.example,
    }

    if args.debug:

        with launch_ipdb_on_exception():
            _solve_puzzles(**solve_puzzle_args)

    elif args.profile:

        with profile(sortby="tottime", amount=20) as _:
            _solve_puzzles(**solve_puzzle_args)

    else:
        _solve_puzzles(**solve_puzzle_args)


if __name__ == "__main__":
    main()
