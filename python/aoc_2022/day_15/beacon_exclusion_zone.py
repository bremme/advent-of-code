def parse(lines):

    result = []

    for line in lines:
        sensor_string, beacon_string = line.split(": ")
        sensor = tuple(
            [
                int(value)
                for value in sensor_string.replace("Sensor at x=", "")
                .replace(" y=", "")
                .split(",")
            ][::-1]
        )
        beacon = tuple(
            [
                int(value)
                for value in beacon_string.replace("closest beacon is at x=", "")
                .replace(" y=", "")
                .split(",")
            ][::-1]
        )
        distance = calculate_manhattan_distance(sensor, beacon)

        result.append((sensor, beacon, distance))

    return result


def calculate_triange_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def is_in_triangle_area(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = calculate_triange_area(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = calculate_triange_area(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = calculate_triange_area(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = calculate_triange_area(x1, y1, x2, y2, x, y)

    # Check if sum of A1, A2 and A3
    # is same as A
    if A == A1 + A2 + A3:
        return True
    else:
        return False


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
