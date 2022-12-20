import argparse
import cProfile
import importlib
import io
import logging
import pstats
import time

from aoc_2022.utils.utils import read_puzzle_input, read_puzzle_input_file
from ipdb import launch_ipdb_on_exception

logger = logging.getLogger()


def _find_puzzles():
    from pathlib import Path

    PACKAGE_ROOT = Path(__file__).parent

    puzzles = {}

    for day in range(1, 25 + 1):
        module_dir = PACKAGE_ROOT / f"day_{day}"
        if not module_dir.exists():
            continue

        puzzles[day] = {"title": "", "variants": {}}

        module_variants = []

        for path in module_dir.iterdir():
            if path.is_dir():
                continue
            if path.name.startswith("__"):
                continue
            if path.name.split(".")[-1] != "py":
                continue
            module_variants.append("".join(path.name.split(".")[:-1]))

        default_module = module_variants.pop(
            module_variants.index(min(module_variants, key=len))
        )

        puzzles[day]["title"] = default_module.replace("_", " ").title()
        puzzles[day]["variants"]["default"] = importlib.import_module(
            f"aoc_2022.day_{day}.{default_module}"
        )
        for module_name in module_variants:
            variant_name = module_name.split("_")[-1]
            puzzles[day]["variants"][variant_name] = importlib.import_module(
                f"aoc_2022.day_{day}.{module_name}"
            )

    return puzzles


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

    return parser.parse_args()


def _setup_logger(verbose):
    # setup logger
    FORMAT = "%(message)s"
    logging.basicConfig(format=FORMAT)

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def _solve_puzzles(day, title, part, module, lines, example):

    logger.info(f"---- Day {day}: {title} ---")

    if part in [1, None]:
        logger.info(f"--- Part One {'Example' if example else ''}---")
        start = time.time()
        answer_part_one = module.solve_part_one(lines, example)
        duration_ms = (time.time() - start) * 1_000
        logger.info(f"Answer part one: {answer_part_one}\t(took {duration_ms:,.3f} ms)")

    if part in [2, None]:
        logger.info(f"--- Part Two {'Example' if example else ''}---")
        start = time.time()
        answer_part_two = module.solve_part_two(lines, example)
        duration_ms = (time.time() - start) * 1_000
        logger.info(f"Answer part two: {answer_part_two}\t(took {duration_ms:,.3f} ms)")


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
    puzzles = _find_puzzles()

    args = _parse_args()

    _setup_logger(args.verbose)

    # read input data
    if args.input_file:
        lines = read_puzzle_input_file(args.input_file)
    else:
        lines = read_puzzle_input(args.day, args.example)

    puzzle = puzzles.get(args.day, None)

    if puzzle is None:
        raise RuntimeError(f"No puzzle defined for day {args.day}")

    module = puzzle["variants"].get(args.variant, None)

    if module is None:
        raise RuntimeError("No module defined for thid variant '{args.variant}'")

    title = puzzle["title"]

    solve_puzzle_args = {
        "day": args.day,
        "title": title,
        "part": args.part,
        "module": module,
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
