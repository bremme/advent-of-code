from aoc_2022.utils import utils


def parse(lines):

    result = []

    for line in lines:
        numbers = utils.parse_integers(line)

        sensor = tuple(reversed(numbers[:2]))

        beacon = tuple(reversed(numbers[2:]))

        distance = calculate_manhattan_distance(sensor, beacon)

        result.append((sensor, beacon, distance))

    return result


def calculate_manhattan_distance(point_one, point_two):
    row_one, column_one = point_one
    row_two, column_two = point_two

    return abs(column_one - column_two) + abs(row_one - row_two)


def does_sensor_beam_intersect(sensor, distance, intersection_row):
    row, _ = sensor

    # intersection is below and beam down intersects
    if row <= intersection_row and (row + distance) >= intersection_row:
        return True

    # intersection is above and beam up intersects
    if row >= intersection_row and (row - distance) <= intersection_row:
        return True

    return False


def calculate_sensor_beam_intersection(sensor, distance, intersection_row):
    row, column = sensor
    half_beam_width = distance - abs(row - intersection_row)

    # special case when only the tip of the beam intersects
    if half_beam_width == 0:
        return [column]

    return [
        column for column in range(column - half_beam_width, column + half_beam_width)
    ]


def calculate_num_positions_which_cant_contain_beacon(data, scan_row):

    positions_with_no_beacon = set()

    for sensor, _, distance in data:

        # check if sensor beam intersects with scan row
        if not does_sensor_beam_intersect(sensor, distance, scan_row):
            continue

        intersection = calculate_sensor_beam_intersection(sensor, distance, scan_row)

        positions_with_no_beacon.update(intersection)

    return len(positions_with_no_beacon)


def calculate_tuning_frequency(beacon):
    row, column = beacon

    return column * 4_000_000 + row


def find_distress_beacon_position(data, max_coordinate):
    pass


def solve_part_one(lines, example):

    scan_row = 10 if example else 2_000_000

    data = parse(lines)

    return calculate_num_positions_which_cant_contain_beacon(data, scan_row=scan_row)


def solve_part_two(lines, example):
    max_coordinate = 20 if example else 4_000_000
