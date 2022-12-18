import argparse
import logging

from aoc_2022.day_11 import monkey_in_the_middle
from aoc_2022.day_12 import hill_climbing_algorithm
from aoc_2022.utils.utils import read_puzzle_input, read_puzzle_input_file
from ipdb import launch_ipdb_on_exception

PUZZLES = {11: "Monkey in the Middle", 12: "Hill Climbing Algorithm"}
MODULES = {11: monkey_in_the_middle, 12: hill_climbing_algorithm}


def main():

    logger = logging.getLogger()

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

    logger.info(f"---- Day {args.day}: {PUZZLES[args.day]} ---")

    def solve_puzzle():
        if args.part in [1, None]:
            answer_part_one = module.solve_part_one(lines)
            logger.info(f"Answer part one: {answer_part_one}")

        if args.part in [2, None]:
            logger.info("--- Part Two ---")
            answer_part_two = module.solve_part_two(lines)
            logger.info(f"Answer part two: {answer_part_two}")

    if args.debug:
        with launch_ipdb_on_exception():
            solve_puzzle()
    else:
        solve_puzzle()


if __name__ == "__main__":
    main()
