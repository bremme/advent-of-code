import argparse
import logging

from aoc_2022.app.creator import Creater
from aoc_2022.app.runner import Runner


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aoc",
        description="CLI interface to run advent of code puzzles.",
    )

    subparsers = parser.add_subparsers(dest="cmd")

    _add_run_parser(subparsers)

    _add_create_parser(subparsers)

    return parser


def _add_run_parser(subparsers):
    run_parser = subparsers.add_parser(
        "run", help="Run a puzzle solution. see `aoc run --help` for more details."
    )

    run_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print more (debugging) output."
    )

    run_parser.add_argument(
        "-d", "--day", type=int, required=True, help="The puzzle day."
    )
    run_parser.add_argument(
        "-p", "--part", type=int, choices=[1, 2], help="Only run part one or two."
    )
    run_parser.add_argument(
        "--variant", default="default", help="Run an alternative variant."
    )
    run_parser.add_argument(
        "-e", "--example", action="store_true", help="Run using example data."
    )

    run_parser.add_argument(
        "-f",
        "--file",
        type=str,
        dest="input_file",
        metavar="FILE",
        help="CHoose an alternative input file",
    )
    run_parser.add_argument(
        "--debug", action="store_true", help="Launch ipdb shell on exception."
    )
    run_parser.add_argument(
        "--profile", action="store_true", help="Profile this run using cProfile."
    )
    run_parser.add_argument(
        "--assert",
        action="store_true",
        dest="assert_answer",
        help="Check the answer(s).",
    )


def _add_create_parser(subparsers):
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new puzzle solution. see `aoc create --help` for more details.",
    )
    create_parser.add_argument(
        "-d", "--day", type=int, required=True, help="The puzzle day."
    )


def main():

    parser = _build_parser()

    args = parser.parse_args()

    if args.cmd == "run":
        Runner(args).run()

    if args.cmd == "create":
        Creater(args).create()

    if args.cmd is None:
        parser.print_help()


if __name__ == "__main__":
    main()
