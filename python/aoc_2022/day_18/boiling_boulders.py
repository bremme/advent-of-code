def parse(lines: list[str]) -> list[list[int]]:
    cubes = []
    for line in lines:
        cube = tuple(map(int, line.split(",")))
        cubes.append(cube)
    return cubes


def solve_part_one(lines: list[str], example: bool):
    cubes = parse(lines)

    # sides of cube = 6
    # when does a cube toch
    # coordinate is the center of the cube I guess
    # two cubes can only touch on one side
    # a cube touches if there is all coordinates are the same except one

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


def solve_part_two(lines: list[str], example: bool):
    answer = 0
    return answer
