import math


def parse(lines: list[str]):
    blueprints = {}
    for line in lines:
        id_number = int(line.split(":")[0].split("Blueprint ")[1])

        ore_cost_ore = int(line.split("ore robot costs ")[1].split()[0])

        clay_cost_ore = int(line.split("clay robot costs ")[1].split()[0])

        obsidian_cost_ore = int(line.split("obsidian robot costs ")[1].split()[0])
        obsidian_cost_clay = int(line.split("obsidian robot costs ")[1].split()[3])

        geode_cost_ore = int(line.split("geode robot costs ")[1].split()[0])
        geode_cost_obsidian = int(line.split("geode robot costs ")[1].split()[3])

        robot_costs = {
            "ore": {"ore": ore_cost_ore},
            "clay": {"ore": clay_cost_ore},
            "obsidian": {"ore": obsidian_cost_ore, "clay": obsidian_cost_clay},
            "geode": {"ore": geode_cost_ore, "obsidian": geode_cost_obsidian},
        }
        max_spend_rates = {
            "ore": max(
                [ore_cost_ore, clay_cost_ore, obsidian_cost_ore, geode_cost_ore]
            ),
            "clay": obsidian_cost_clay,
            "obsidian": geode_cost_obsidian,
        }

        blueprints[id_number] = {
            "robot_costs": robot_costs,
            "max_spend_rates": max_spend_rates,
        }

    return blueprints


def can_robot_be_build(costs, robots, resources):
    wait = 0

    # Can we build this robot?
    for resource, amount in costs.items():
        # continue if we already have the resources
        if resources[resource] >= amount:
            max(0, wait)
            continue
        # If we don't have robots collecting this resource we can never build this robot
        if robots[resource] == 0:
            return False, wait
        # How long will it take to collect the required amount of resource
        # take the max to deal with negative values -> we already have enough
        wait = max(wait, math.ceil((amount - resources[resource]) / robots[resource]))

    # we are able to wait for this robot
    return True, wait


def solve_dfs(
    time_remaining,
    robots: dict,
    resources: dict,
    robot_costs,
    max_spend_rates: dict,
    cache,
    geode_at_time,
    calls=0,
):
    calls += 1
    # not time_remaining
    if time_remaining == 0:
        return resources["geode"], calls

    # if we do nothing
    max_amount_geode = resources["geode"] + robots["geode"] * time_remaining

    # Optimization
    # check if we have already processed a state for the same minute with higher amount of geode
    if geode_at_time.get(time_remaining, 0) > resources["geode"]:
        return max_amount_geode, calls

    cache_index = tuple([time_remaining, *robots.values(), *resources.values()])

    if cache_index in cache:
        return cache[cache_index], calls

    # what happend when we build new robots
    for robot_type, costs in robot_costs.items():
        # Optimization: Do we need to build this robot?
        # always build geode collector robots
        # do we already have enough collector robot to supply our maximum spend rate
        if robot_type != "geode" and (
            robots[robot_type] * time_remaining + resources[robot_type]
        ) >= (max_spend_rates[robot_type] * time_remaining):
            continue

        can_be_build, wait = can_robot_be_build(costs, robots, resources)

        if can_be_build is False:
            continue

        time_to_build_robot = 1
        new_time_remaining = time_remaining - wait - time_to_build_robot

        # If there is no time left, no point in building this robot
        if new_time_remaining <= 0:
            continue

        new_robots = robots.copy()
        new_resources = {}

        # Calculate resources
        for resource, number_of_robots in new_robots.items():
            new_resources[resource] = (
                resources[resource] + (wait + time_to_build_robot) * number_of_robots
            )

        # spend resource to build robot
        for resource, amount in costs.items():
            new_resources[resource] -= amount

        # build the robot
        new_robots[robot_type] += 1

        # optimization: it makes no sense to have more resources then the max we can
        # spend each turn
        for resource, max_spend_rate in max_spend_rates.items():
            new_resources[resource] = min(
                new_resources[resource],
                max_spend_rate * time_remaining,
            )

        new_max_amount_geode, calls = solve_dfs(
            time_remaining=new_time_remaining,
            robots=new_robots,
            resources=new_resources,
            robot_costs=robot_costs,
            max_spend_rates=max_spend_rates,
            cache=cache,
            geode_at_time=geode_at_time,
            calls=calls,
        )
        max_amount_geode = max(max_amount_geode, new_max_amount_geode)

    cache[cache_index] = max_amount_geode
    geode_at_time[time_remaining] = max(
        geode_at_time.get(time_remaining, 0), resources["geode"]
    )

    return max_amount_geode, calls


def solve_part_one(lines: list[str], example: bool) -> int:
    blueprints = parse(lines)

    robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}

    total_quality_level = 0

    for id_, blueprint in blueprints.items():
        robot_costs = blueprint["robot_costs"]
        max_spend_rates = blueprint["max_spend_rates"]
        solution, calls = solve_dfs(
            24, robots, resources, robot_costs, max_spend_rates, {}, {}
        )
        quality_level = id_ * solution
        print(
            f"quaility level {id_} = {quality_level} (solutions = {solution}, calls = {calls})"
        )
        total_quality_level += quality_level

    return total_quality_level


def solve_part_two(lines: list[str], example: bool) -> int:
    answer = 0
    return answer
