import unittest

from aoc_2022.utils import utils


class TestUtils(unittest.TestCase):
    def test_read_positive_integers(self):
        lines = [
            ("1000", [1000]),  # day 1
            ("9-43,8-44", [9, 43, 8, 44]),  # day 4
            ("move 1 from 2 to 1", [1, 2, 1]),  # day 5
            ("14848514 b.txt", [14848514]),  # day 7
            ("R 4", [4]),  # day 9
            ("  Starting items: 54, 65, 75, 74", [54, 65, 75, 74]),  # day 11
            (
                "503,4 -> 502,4 -> 502,9 -> 494,9",
                [503, 4, 502, 4, 502, 9, 494, 9],
            ),  # day 14
            (
                "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
                [17, 20, 21, 22],
            ),  # day 15
        ]

        for line, result in lines:
            self.assertEqual(utils.read_positive_integers(line), result)

    def test_read_integers(self):
        lines = [
            ("9-43,8-44", [9, -43, 8, -44]),  # day 4
            ("addx 13", [13]),  # day 10
            ("addx -35", [-35]),  # day 10
        ]

        for line, result in lines:
            self.assertEqual(utils.read_integers(line), result)


if __name__ == "__main__":
    unittest.main()
