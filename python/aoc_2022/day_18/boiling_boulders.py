def parse(lines: list[str]) -> list[list[int]]:
    cubes = []
    for line in lines:
        cube = tuple(map(int, line.split(",")))
        cubes.append(cube)
    return cubes


def solve_one(cubes):

    surface_area = len(cubes) * 6

    for i, cube in enumerate(cubes):
        for j, other_cube in enumerate(cubes):
            if cube == other_cube:
                continue
            #
            x1, y1, z1 = cube
            x2, y2, z2 = other_cube

            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            dz = abs(z1 - z2)

            if sum([dx, dy, dz]) == 1:
                surface_area -= 1

    return surface_area


def cube_is_connected(cube, other_cube):
    x1, y1, z1 = cube
    x2, y2, z2 = other_cube

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dz = abs(z1 - z2)

    if sum([dx, dy, dz]) == 1:
        return True

    return False


def solve_two(cubes):
    # cubes_x = sorted(cubes, key=lambda c: c[0])
    # cubes_y = sorted(cubes, key=lambda c: c[1])
    # cubes_z = sorted(cubes, key=lambda c: c[2])

    cubes_x = {}
    cubes_y = {}
    cubes_z = {}

    for cube in cubes:
        x, y, z = cube

        if x not in cubes_x:
            cubes_x[x] = []
        if y not in cubes_y:
            cubes_y[y] = []
        if z not in cubes_z:
            cubes_z[z] = []

        cubes_x[x].append(cube)
        cubes_y[y].append(cube)
        cubes_z[z].append(cube)

    # dict with x coordinates and all cubes with those
    # dict with y coordiantes and all cubes with those

    surface_area = len(cubes) * 6

    data = {0: cubes_x, 1: cubes_y, 2: cubes_z}

    for cube in cubes:
        x, y, z = cube

        for direction in [0, 1, 2]:
            for delta in [-1, 1]:
                for other_cube in data[direction].get(cube[direction] + delta, []):
                    if cube_is_connected(cube, other_cube):
                        surface_area -= 1
                        break

        continue

        # look for touching cubes in x
        for cube_x in cubes_x.get(x - 1, []) + cubes_x.get(x + 1, []):
            if cube_is_connected(cube, cube_x):
                surface_area -= 1

        # if (x + 1) in cubes_x:
        #     for cube_x in cubes_x[x + 1]:
        #         if cube_is_connected(cube, cube_x):
        #             surface_area -= 1

        # look for touching cubes in y
        if (y - 1) in cubes_y:
            for cube_y in cubes_y[y - 1]:
                if cube_is_connected(cube, cube_y):
                    surface_area -= 1

        if (y + 1) in cubes_y:
            for cube_y in cubes_y[y + 1]:
                if cube_is_connected(cube, cube_y):
                    surface_area -= 1

        # look for touching cubes in z
        if (z - 1) in cubes_z:
            for cube_z in cubes_z[z - 1]:
                if cube_is_connected(cube, cube_z):
                    surface_area -= 1

        if (z + 1) in cubes_z:
            for cube_z in cubes_z[z + 1]:
                if cube_is_connected(cube, cube_z):
                    surface_area -= 1

    return surface_area


def solve_part_one(lines: list[str], example: bool):
    cubes = parse(lines)

    # sides of cube = 6
    # when does a cube touch?
    # coordinate is the center of the cube I guess
    # two cubes can only touch on one side
    # a cube touches if there is all coordinates are the same except one
    # return solve_one(cubes)

    return solve_two(cubes)


def solve_part_two(lines: list[str], example: bool):
    answer = 0
    return answer
