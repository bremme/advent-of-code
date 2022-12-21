import unittest

from aoc_2022.day_10.cathode_ray_tube import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 10
YEAR = 2022


class TestRopeBridge(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 13140)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 14420)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        expected_answer = [
            "⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫⚪⚪⚫⚫",
            "⚪⚪⚪⚫⚫⚫⚪⚪⚪⚫⚫⚫⚪⚪⚪⚫⚫⚫⚪⚪⚪⚫⚫⚫⚪⚪⚪⚫⚫⚫⚪⚪⚪⚫⚫⚫⚪⚪⚪⚫",
            "⚪⚪⚪⚪⚫⚫⚫⚫⚪⚪⚪⚪⚫⚫⚫⚫⚪⚪⚪⚪⚫⚫⚫⚫⚪⚪⚪⚪⚫⚫⚫⚫⚪⚪⚪⚪⚫⚫⚫⚫",
            "⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫",
            "⚪⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪",
            "⚪⚪⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪⚪⚫⚫⚫⚫⚫",
        ]

        crt = solve_part_two(lines)

        for row, expected_row in enumerate(expected_answer):
            row = "".join(crt.frame_buffer[row])
            self.assertEqual(row, expected_row)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        expected_answer = [
            "⚪⚪⚪⚫⚫⚫⚪⚪⚫⚫⚪⚫⚫⚫⚫⚪⚪⚪⚫⚫⚪⚪⚪⚫⚫⚪⚪⚪⚪⚫⚫⚪⚪⚫⚫⚪⚫⚫⚪⚫",
            "⚪⚫⚫⚪⚫⚪⚫⚫⚪⚫⚪⚫⚫⚫⚫⚪⚫⚫⚪⚫⚪⚫⚫⚪⚫⚫⚫⚫⚪⚫⚪⚫⚫⚪⚫⚪⚫⚫⚪⚫",
            "⚪⚫⚫⚪⚫⚪⚫⚫⚫⚫⚪⚫⚫⚫⚫⚪⚫⚫⚪⚫⚪⚪⚪⚫⚫⚫⚫⚪⚫⚫⚪⚫⚫⚪⚫⚪⚫⚫⚪⚫",
            "⚪⚪⚪⚫⚫⚪⚫⚪⚪⚫⚪⚫⚫⚫⚫⚪⚪⚪⚫⚫⚪⚫⚫⚪⚫⚫⚪⚫⚫⚫⚪⚪⚪⚪⚫⚪⚫⚫⚪⚫",
            "⚪⚫⚪⚫⚫⚪⚫⚫⚪⚫⚪⚫⚫⚫⚫⚪⚫⚪⚫⚫⚪⚫⚫⚪⚫⚪⚫⚫⚫⚫⚪⚫⚫⚪⚫⚪⚫⚫⚪⚫",
            "⚪⚫⚫⚪⚫⚫⚪⚪⚪⚫⚪⚪⚪⚪⚫⚪⚫⚫⚪⚫⚪⚪⚪⚫⚫⚪⚪⚪⚪⚫⚪⚫⚫⚪⚫⚫⚪⚪⚫⚫",
        ]

        crt = solve_part_two(lines)

        for row, expected_row in enumerate(expected_answer):
            row = "".join(crt.frame_buffer[row])
            self.assertEqual(row, expected_row)


if __name__ == "__main__":
    unittest.main()
