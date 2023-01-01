from collections import deque

directions = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def parse(
    lines: list[str],
) -> tuple[set[tuple[int, ...]], tuple[int, int, int, int, int, int]]:
    cubes = []
    for line in lines:
        cube = tuple(map(int, line.split(",")))
        cubes.append(cube)

    x = [x for x, _, _ in cubes]
    y = [y for _, y, _ in cubes]
    z = [z for _, _, z in cubes]
    min_x, min_y, min_z = min(x), min(y), min(z)
    max_x, max_y, max_z = max(x), max(y), max(z)

    shape = min_x, max_x, min_y, max_y, min_z, max_z

    return set(cubes), shape


def is_exterior_surface(x: int, y: int, z: int, cubes, shape, cache):

    if (x, y, z) in cache:
        return cache[x, y, z]

    # store initial coordinates for caching later
    x0, y0, z0 = x, y, z

    x_min, x_max, y_min, y_max, z_min, z_max = shape

    queue = deque()

    seen = set()

    queue.append((x, y, z))

    while queue:
        x, y, z = queue.popleft()

        if (x, y, z) in seen:
            continue

        seen.add((x, y, z))

        if (x, y, z) in cubes:
            continue

        if x < x_min or x > x_max or y < y_min or y > y_max or z < z_min or z > z_max:
            cache[(x0, y0, z0)] = True
            return True

        for dx, dy, dz in directions:
            queue.append((x + dx, y + dy, z + dz))

    cache[(x0, y0, z0)] = False

    return False


def solve_part_one(lines: list[str], example: bool) -> int:
    cubes, _ = parse(lines)

    surface_area = 0

    # loop over cube (coordinates)
    for x, y, z in cubes:
        # loop over directions
        for dx, dy, dz in directions:
            # calculate neighbour position
            neighbour = (x + dx, y + dy, z + dz)
            # check if neigbour exist
            if neighbour not in cubes:
                surface_area += 1

    return surface_area


def solve_part_two(lines: list[str], example: bool) -> int:
    cubes, shape = parse(lines)

    surface_area: int = 0
    cache: dict[tuple[int, int, int], bool] = {}

    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in directions:
            if is_exterior_surface(x + dx, y + dy, z + dz, cubes, shape, cache):
                surface_area += 1

    return surface_area
