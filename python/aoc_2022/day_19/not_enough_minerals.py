import math
from decimal import MAX_EMAX


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


def solve_dfs(
    time_remaining,
    robots: dict,
    resources: dict,
    robot_costs,
    max_spend_rates: dict,
    cache,
):
    # not time_remaining
    if time_remaining == 0:
        return resources["geode"]

    key = tuple([time_remaining, *robots.values(), *resources.values()])

    if key in cache:
        return cache[key]

    # if we do nothing
    max_amount_geode = resources["geode"] + robots["geode"] * time_remaining

    # what happend when we build new robots
    for robot_type, costs in robot_costs.items():
        # do we want to build this robot?
        # we always want to build geode robots
        # we don't want / can't? build robots when we are over the max costs?
        if robot_type != "geode" and robots[robot_type] >= max_spend_rates[robot_type]:
            continue

        # how long do we have to wait to build this robot
        wait = 0

        for resource, amount in costs.items():
            # If we don't have robots collecting this resource we can't build this robot
            if robots[resource] == 0:
                break
            # How long will it take to collect the required amount of resource
            # take the max to deal with negative values -> we already have enough
            wait = max(
                wait, math.ceil((amount - resources[resource]) / robots[resource])
            )
        # we are able to wait for this robot (it did not break)
        else:
            time_to_build_robot = 1
            new_time_remaining = time_remaining - wait - time_to_build_robot

            if new_time_remaining <= 0:
                continue

            new_robots = robots.copy()
            new_resources = {}

            for resource, number_of_robots in new_robots.items():
                new_resources[resource] = (
                    resources[resource]
                    + (wait + time_to_build_robot) * number_of_robots
                )

            # spend resource to build robot
            for resource, amount in costs.items():
                new_resources[resource] -= amount

            # build the robot
            new_robots[robot_type] += 1

            # optimization: it makes no sense to have more resources then the max we can spend each turn
            for resource, max_spend_rate in max_spend_rates.items():
                new_resources[resource] = min(
                    new_resources[resource],
                    max_spend_rate * time_remaining,
                )

            max_amount_geode = max(
                max_amount_geode,
                solve_dfs(
                    time_remaining=new_time_remaining,
                    robots=new_robots,
                    resources=new_resources,
                    robot_costs=robot_costs,
                    max_spend_rates=max_spend_rates,
                    cache=cache,
                ),
            )

    cache[key] = max_amount_geode

    return max_amount_geode


def solve_part_one(lines: list[str], example: bool) -> int:
    blueprints = parse(lines)

    blueprint_id = 1

    # print(blueprints)

    def can_robot_be_afforded(robot_type, robot_costs, resources):
        for resource, cost in robot_costs.items():
            if resources[resource] < cost:
                return False
        return True

    def pay_for_robot(robot_cost, resources):
        for resource, cost in robot_cost.items():
            resources[resource] -= cost
        return resources

    robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}

    resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}

    total_quality_level = 0

    for id_, blueprint in blueprints.items():
        robot_costs = blueprint["robot_costs"]
        max_spend_rates = blueprint["max_spend_rates"]
        solution = solve_dfs(24, robots, resources, robot_costs, max_spend_rates, {})
        quality_level = id_ * solution
        print(f"quaility level {id_} = {quality_level} ({solution})")
        total_quality_level += quality_level

    return total_quality_level

    # robot_types_to_build = ["geode", "obsidian", "clay", "ore"]

    # build_robot_type = None

    # for minute in range(1, 24 + 1):

    #     print(f"== Minute {minute} ==")

    #     # determine which robot to build
    #     for robot_type in robot_types_to_build:
    #         if can_robot_be_afforded(robot_type, robot_costs[robot_type], resources):
    #             print(
    #                 f"Spend {robot_costs[robot_type]} to start building a {robot_type} collector robot"
    #             )
    #             resources = pay_for_robot(robot_costs[robot_type], resources)
    #             build_robot_type = robot_type
    #             break

    #         build_robot_type = None

    #     # collect resources
    #     for resource, amount in robots.items():
    #         resources[resource] += amount
    #         if amount == 0:
    #             continue
    #         print(
    #             f"{amount} {resource}-collecting robots collect {amount} {resource}; you now have {resources[resource]}."
    #         )

    #     # finishe building new collectors
    #     if build_robot_type:
    #         robots[build_robot_type] += 1
    #         print(
    #             f"The new {build_robot_type}-collecting robot is ready; you now have {robots[build_robot_type]} of them."
    #         )
    #     if minute == 11:
    #         return

    return 0


def solve_part_two(lines: list[str], example: bool) -> int:
    answer = 0
    return answer
