import argparse
import logging

from aoc_2022.app.runner import Runner


def _parse_args():
    parser = argparse.ArgumentParser(
        prog="aoc",
        description="CLI interface to run advent of code puzzles.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    subparsers = parser.add_subparsers(dest="cmd")
    run_parser = subparsers.add_parser("run")

    run_parser.add_argument("-d", "--day", type=int, required=True)
    run_parser.add_argument("-p", "--part", type=int)
    run_parser.add_argument("--variant", default="default")
    run_parser.add_argument("-e", "--example", action="store_true")

    run_parser.add_argument("-f", "--file", type=str, dest="input_file")
    run_parser.add_argument("--debug", action="store_true")
    run_parser.add_argument("--profile", action="store_true")
    run_parser.add_argument("--assert", action="store_true", dest="assert_answer")

    return parser.parse_args()


def _setup_logger(verbose):
    # setup logger
    FORMAT = "%(message)s"
    logging.basicConfig(format=FORMAT)

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def main():

    args = _parse_args()

    _setup_logger(args.verbose)

    if args.cmd == "run":
        Runner(args).run()


if __name__ == "__main__":
    main()
