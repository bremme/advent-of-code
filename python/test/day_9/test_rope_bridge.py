import unittest

from aoc.day_9.rope_bridge import (
    calculate_tail_movement,
    determine_playground,
    determine_playground_2,
    parse_series_of_motions,
    solve_part_one,
)
from aoc.utils import utils

DAY = 9
YEAR = 2022


class TestRopeBridge(unittest.TestCase):
    # def test_calculate_tail_movement(self):

    #     head = (4, 2)
    #     tail = (3, 0)
    #     direction = calculate_tail_movement(head, tail)

    #     breakpoint()

    # def test_point_touches_other_point(self):
    #     #  1,3    2,3     3,3
    #     #  1,2    2,2     3,2
    #     #  1,1    2,1     3,1

    #     point = 2, 2
    #     touching_other_points = [
    #         (1, 1),
    #         (2, 1),
    #         (3, 1),
    #         (1, 2),
    #         (3, 2),
    #         (1, 3),
    #         (2, 3),
    #         (3, 3),
    #     ]

    #     for other_point in touching_other_points:
    #         touches = point_touches_other_point(point, other_point)
    #         self.assertTrue(touches)

    #     non_touching_other_points = [(4, 1), (1, 4), (2, 4)]
    #     for other_point in non_touching_other_points:
    #         touches = point_touches_other_point(point, other_point)
    #         self.assertFalse(touches)

    def test_determine_playground_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)
        series_of_motions = parse_series_of_motions(lines)

        start, (rows, columns) = determine_playground_2(series_of_motions)

        self.assertEqual((start.row, start.col), (0, 0))
        self.assertEqual((rows, columns), (5, 6))

    def test_determine_playground(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)
        series_of_motions = parse_series_of_motions(lines)

        start, (rows, columns) = determine_playground_2(series_of_motions)

        self.assertEqual((start.row, start.col), (16, 225))
        self.assertEqual((rows, columns), (520, 233))

    # def test_solve_part_one_example(self):
    #     lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

    #     answer = solve_part_one(lines)

    #     self.assertEqual(answer, 13)

    # def test_solve_part_one(self):
    #     lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

    #     answer = solve_part_one(lines)

    #     self.assertEqual(answer, 6391)

    # def test_solve_part_two_example(self):
    #     lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

    #     answer = solve_part_two(lines)

    #     self.assertEqual(answer, "MCD")

    # def test_solve_part_two(self):
    #     lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

    #     answer = solve_part_two(lines)

    #     self.assertEqual(answer, "CDTQZHBRS")


if __name__ == "__main__":
    unittest.main()
