import argparse
import logging
import time

from aoc_2022.day_11 import monkey_in_the_middle
from aoc_2022.day_12 import hill_climbing_algorithm
from aoc_2022.day_13 import distress_signal
from aoc_2022.utils.utils import read_puzzle_input, read_puzzle_input_file
from ipdb import launch_ipdb_on_exception

PUZZLES = {
    11: "Monkey in the Middle",
    12: "Hill Climbing Algorithm",
    13: "Distress Signal",
}
MODULES = {11: monkey_in_the_middle, 12: hill_climbing_algorithm, 13: distress_signal}

logger = logging.getLogger()


def _solve_puzzles(day, part, module, lines):

    logger.info(f"---- Day {day}: {PUZZLES[day]} ---")

    if part in [1, None]:
        logger.info("--- Part One ---")
        start = time.time()
        answer_part_one = module.solve_part_one(lines)
        duration_ms = (time.time() - start) * 1_000
        logger.info(f"Answer part one: {answer_part_one}\t(took {duration_ms:,.3f} ms)")

    if part in [2, None]:
        logger.info("--- Part Two ---")
        start = time.time()
        answer_part_two = module.solve_part_two(lines)
        duration_ms = (time.time() - start) * 1_000
        logger.info(f"Answer part two: {answer_part_two}\t(took {duration_ms:,.3f} ms)")


def main():

    parser = argparse.ArgumentParser(prog="Advent of Code")

    parser.add_argument("-d", "--day", type=int, required=True)
    parser.add_argument("-p", "--part", type=int)
    parser.add_argument("-e", "--example", action="store_true")

    parser.add_argument("-f", "--file", type=str, dest="input_file")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    # read input data
    if args.input_file:
        lines = read_puzzle_input_file(args.input_file)
    else:
        lines = read_puzzle_input(args.day, args.example)

    # setup logger
    FORMAT = "%(message)s"
    logging.basicConfig(format=FORMAT)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    module = MODULES.get(args.day)

    if args.debug:
        with launch_ipdb_on_exception():
            _solve_puzzles(day=args.day, part=args.part, module=module, lines=lines)
    else:
        _solve_puzzles(day=args.day, part=args.part, module=module, lines=lines)


if __name__ == "__main__":
    main()
