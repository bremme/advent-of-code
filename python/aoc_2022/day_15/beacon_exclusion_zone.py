from numpy import half


def parse(lines):

    result = []

    for line in lines:
        sensor_string, beacon_string = line.split(": ")
        sensor = [
            int(value)
            for value in sensor_string.replace("Sensor at x=", "")
            .replace(" y=", "")
            .split(",")
        ][::-1]
        beacon = [
            int(value)
            for value in beacon_string.replace("closest beacon is at x=", "")
            .replace(" y=", "")
            .split(",")
        ][::-1]
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


def calculate_num_positions_which_cant_contain_beacon(data, scan_row):

    positions_with_no_beacon = set()

    for sensor, beacon, distance in data:
        row, column = sensor
        # check if this sensor can scan up to this row
        if (row + distance) < scan_row and (row - distance) > scan_row:
            continue

        half_width = distance - abs(row - scan_row)

        for column in range(column - half_width, column + half_width):
            positions_with_no_beacon.add((scan_row, column))

    return len(positions_with_no_beacon)


def solve_part_one(lines):
    data = parse(lines)
    return calculate_num_positions_which_cant_contain_beacon(data, scan_row=2000000)

    # grid = [["."] * columns for _ in range(rows)]


def solve_part_two(lines):
    pass
