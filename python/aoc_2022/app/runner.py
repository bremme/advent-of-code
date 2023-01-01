import cProfile
import io
import logging
import pstats
import time

from aoc_2022 import PACKAGE_ROOT
from aoc_2022.app.puzzle_finder import PuzzleFinder
from aoc_2022.utils import utils
from aoc_2022.utils.utils import read_puzzle_input, read_puzzle_input_file
from ipdb import launch_ipdb_on_exception

logger = logging.getLogger()


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


class Runner:
    def __init__(self, args):

        # get puzzle
        self.puzzle = PuzzleFinder.find_puzzles(PACKAGE_ROOT).get_puzzle(args.day)
        self.variant = args.variant
        self.part = args.part
        self.example = args.example

        self.year = 2022

        self.debug = args.debug
        self.profile = args.profile
        self.assert_answer = args.assert_answer

        # read input data
        if args.input_file:
            self.lines = read_puzzle_input_file(args.input_file)
        else:
            self.lines = read_puzzle_input(args.day, 2022, args.example)

        # setup logger
        FORMAT = "%(message)s"
        logging.basicConfig(format=FORMAT)

        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def run(self):

        if self.debug:

            with launch_ipdb_on_exception():
                self._solve_puzzle()

        elif self.profile:

            with profile(sortby="tottime", amount=20) as _:
                self._solve_puzzle()

        else:
            self._solve_puzzle()

    def _solve_puzzle(self):
        solution = self.puzzle.get_solution(self.variant)

        logger.info(f"---- Day {self.puzzle.day}: {self.puzzle.title} ---")

        if self.part in [1, None]:
            logger.info(f"--- Part One {'Example' if self.example else ''}---")
            start = time.time()
            answer_part_one = solution.module.solve_part_one(self.lines, self.example)
            duration_ms = (time.time() - start) * 1_000
            logger.info(
                f"Answer part one: {answer_part_one}\t(took {duration_ms:,.3f} ms)"
            )

            if self.assert_answer:
                self._check_puzzle_answer(
                    part=1,
                    answer=answer_part_one,
                )

        if self.part in [2, None]:
            logger.info(f"--- Part Two {'Example' if self.example else ''}---")
            start = time.time()
            answer_part_two = solution.module.solve_part_two(self.lines, self.example)
            duration_ms = (time.time() - start) * 1_000
            logger.info(
                f"Answer part two: {answer_part_two}\t(took {duration_ms:,.3f} ms)"
            )

            if self.assert_answer:
                self._check_puzzle_answer(
                    part=2,
                    answer=answer_part_two,
                )

    def _check_puzzle_answer(self, part, answer):

        day = self.puzzle.day
        year = self.year
        example = self.example

        expected_answer = utils.read_puzzle_answer(
            day=day, year=year, part=part, example=example
        )

        if answer != expected_answer:
            raise AssertionError(f"{answer} != {expected_answer}")

        logger.info(
            f"Assertion of answer was successfull ({answer} == {expected_answer})"
        )
