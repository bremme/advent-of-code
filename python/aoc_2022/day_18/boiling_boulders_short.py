def parse(lines: list[str]) -> list[list[int]]:
    cubes = []
    for line in lines:
        cube = tuple(map(int, line.split(",")))
        cubes.append(cube)
    return cubes


def cube_is_connected(cube, other_cube):
    x1, y1, z1 = cube
    x2, y2, z2 = other_cube

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dz = abs(z1 - z2)

    if sum([dx, dy, dz]) == 1:
        return True

    return False


def calculate_surface_area(cubes):
    directions = [
        (-1, 0, 0),
        (1,0,0),
        (0,-1,0),
        (0,1,0),
        (0,0,-1),
        (0,0,1)
    ]

    # build dictionairy with list of cubes for all x, y, z coordinates
    cube_coordinates = {"x": {}, "y": {}, "z": {}}

    for cube in cubes:
        x, y, z = cube.values()

        if x not in cube_coordinates["x"]:
            cube_coordinates["x"][x] = []
        if y not in cube_coordinates["y"]:
            cube_coordinates["y"][y] = []
        if z not in cube_coordinates["z"]:
            cube_coordinates["z"][z] = []

        cube_coordinates["x"][x].append(cube)
        cube_coordinates["y"][y].append(cube)
        cube_coordinates["z"][z].append(cube)

    # start with maximum surface area
    surface_area = len(cubes) * 6

    for cube in cubes:

        # loop over directions x, y, z
        for direction in ["x", "y", "z"]:
            # look both in the negative and positive direction (e.g. left and right)
            for delta in [-1, 1]:

                other_cubes = cube_coordinates[direction].get(
                    cube[direction] + delta, []
                )

                for other_cube in other_cubes:
                    # if we found a connected cube in this direction we break out of
                    # the loop
                    if cube_is_connected(cube, other_cube):
                        surface_area -= 1
                        break
    return surface_area


def solve_part_one(lines: list[str], example: bool):
    cubes = parse(lines)

    # sides of cube = 6
    # when does a cube touch?
    # coordinate is the center of the cube I guess
    # two cubes can only touch on one side
    # a cube touches if there is all coordinates are the same except one
    # return solve_one(cubes)

    return calculate_surface_area(cubes)


def solve_part_two(lines: list[str], example: bool):
    cubes = parse(lines)
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
    for cube in cubes:




    return answer
