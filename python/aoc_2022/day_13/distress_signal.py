import json
import logging

logger = logging.getLogger()


def parse_handheld_packets(lines):

    for index in range(0, len(lines), 3):
        first_packet = json.loads(lines[index])
        second_packet = json.loads(lines[index + 1])
        yield first_packet, second_packet


def values_are_in_the_right_order(left, right, level=1):
    indent_char = "  "
    if level == 10:
        return
    indent = "".join([indent_char] * level)
    logger.debug(f"{indent}- Compare {left} vs {right}")

    type_left = type(left)
    type_right = type(right)

    if type_left is int and type_right is int:
        if left < right:
            indent += indent_char
            logger.debug(
                f"{indent}- Left side is smaller, so inputs are in the right order"
            )
            return True
        if left > right:
            logger.debug(
                f"{indent}- Right side is smaller, so inputs are not in the right order"
            )
            return False
        return None

    if type_left is list and type_right is list:

        length_left = len(left)
        length_right = len(right)

        for new_left, new_right in zip(left, right):

            result = values_are_in_the_right_order(new_left, new_right, level + 1)

            if result is not None:
                return result

        # we have run out of items
        if length_left == length_right:
            return None

        if length_right > length_left:
            return True

        return False

    indent += indent_char

    if type_left is int:
        logger.debug(
            f"{indent}- Mixed types; convert left to [{left}] and retry comparison"
        )
        return values_are_in_the_right_order([left], right, level + 1)

    # right should be an int
    logger.debug(
        f"{indent}- Mixed types; convert right to [{right}] and retry comparison"
    )
    return values_are_in_the_right_order(left, [right], level + 1)


def solve_part_one(lines):
    packet_pair_index = 1

    packet_pairs_results = {True: [], False: []}

    for first_packet, second_packet in parse_handheld_packets(lines):

        logger.debug(f"== Pair {packet_pair_index} ==")

        result = values_are_in_the_right_order(first_packet, second_packet)

        packet_pairs_results[result].append(packet_pair_index)

        packet_pair_index += 1

    return sum(packet_pairs_results[True])


def solve_part_two(lines):
    pass
