import unittest

from aoc_2022.day_9.rope_bridge import (
    calculate_tail_movement,
    point_touches_other_point,
)
from aoc_2022.utils import utils

DAY = 9


class TestRopeBridge(unittest.TestCase):
    def test_calculate_tail_movement(self):

        head = (4, 2)
        tail = (3, 0)
        direction = calculate_tail_movement(head, tail)

        breakpoint()

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

    # def test_solve_part_one_example(self):
    #     lines = utils.read_puzzle_input(day=DAY, example=True)

    #     answer = solve_part_one(lines)

    #     self.assertEqual(answer, "CMZ")

    # def test_solve_part_one(self):
    #     lines = utils.read_puzzle_input(day=DAY, example=False)

    #     answer = solve_part_one(lines)

    #     self.assertEqual(answer, "SHQWSRBDL")

    # def test_solve_part_two_example(self):
    #     lines = utils.read_puzzle_input(day=DAY, example=True)

    #     answer = solve_part_two(lines)

    #     self.assertEqual(answer, "MCD")

    # def test_solve_part_two(self):
    #     lines = utils.read_puzzle_input(day=DAY, example=False)

    #     answer = solve_part_two(lines)

    #     self.assertEqual(answer, "CDTQZHBRS")
