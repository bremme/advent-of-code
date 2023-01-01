def parse(lines: list[str]) -> list[tuple[int, ...]]:
    cubes = []
    for line in lines:
        cube = tuple(map(int, line.split(",")))
        cubes.append(cube)
    return cubes


def get_cube_coordinates(cubes):
    # build dictionairy with list of cubes for all x, y, z coordinates
    cube_coordinates = {"x": {}, "y": {}, "z": {}}

    for cube in cubes:
        x, y, z = cube

        if x not in cube_coordinates["x"]:
            cube_coordinates["x"][x] = []
        if y not in cube_coordinates["y"]:
            cube_coordinates["y"][y] = []
        if z not in cube_coordinates["z"]:
            cube_coordinates["z"][z] = []

        cube_coordinates["x"][x].append(cube)
        cube_coordinates["y"][y].append(cube)
        cube_coordinates["z"][z].append(cube)

    return cube_coordinates


def cube_is_connected(cube, other_cube):
    x1, y1, z1 = cube
    x2, y2, z2 = other_cube

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dz = abs(z1 - z2)

    if sum([dx, dy, dz]) == 1:
        return True

    return False


def calculate_surface_area(cubes, cube_coordinates):
    # start with maximum surface area
    surface_area = len(cubes) * 6

    for cube in cubes:
        # loop over directions x, y, z
        for direction, index in zip(["x", "y", "z"], [0, 1, 2]):
            # look both in the negative and positive direction (e.g. left and right)
            for offset in [-1, 1]:

                # get other cubes with the given offset in the given driection
                other_cubes = cube_coordinates[direction].get(cube[index] + offset, [])

                for other_cube in other_cubes:
                    # if we found a connected cube in this direction we break out of
                    # the loop, since there can only be one in any given direction
                    if cube_is_connected(cube, other_cube):
                        surface_area -= 1
                        break
    return surface_area


def solve_part_one(lines: list[str], example: bool):
    cubes = parse(lines)
    cube_coordinates = get_cube_coordinates(cubes)

    # sides of cube = 6
    # when does a cube touch?
    # coordinate is the center of the cube I guess
    # two cubes can only touch on one side
    # a cube touches if there is all coordinates are the same except one
    # return solve_one(cubes)

    return calculate_surface_area(cubes, cube_coordinates)


def solve_part_two(lines: list[str], example: bool):
    cubes = set(parse(lines))

    surface_area = 0

    # x = [x for x, y, z in cubes]
    # y = [y for x, y, z in cubes]
    # z = [z for x, y, z in cubes]
    # min_x, min_y, min_z = min(x), min(y), min(z)
    # max_x, max_y, max_z = max(x), max(y), max(z)

    directions = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]

    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in directions:
            if (x + dx, y + dy, z + dz) not in cubes:
                surface_area += 1

    # find air bubbles
    # assumme only single cube air bubble
    # when have we found an air bubble?
    # when there is a coordinate which has
    # a cube to the left, right, top, bottom, fron and rear

    # x, y, z

    # left:   x - 1, y, z
    # right:  z + 1, y, z
    # top:

    # find air bubbles
    return surface_area
