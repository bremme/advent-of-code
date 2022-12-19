import json
import logging

logger = logging.getLogger()


def parse_handheld_packets(lines):

    for index in range(0, len(lines), 3):
        first_packet = json.loads(lines[index])
        second_packet = json.loads(lines[index + 1])
        yield first_packet, second_packet


def are_in_order(left, right, level=1):
    INDENT_CHAR = "  "
    indent = "".join([INDENT_CHAR] * level)

    logger.debug(f"{indent}- Compare {left} vs {right}")

    type_left = type(left)
    type_right = type(right)

    # Equal types int
    if type_left is int and type_right is int:
        if left < right:
            indent += INDENT_CHAR
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

    # Equal types list
    if type_left is list and type_right is list:

        for new_left, new_right in zip(left, right):

            result = are_in_order(new_left, new_right, level + 1)

            if result is not None:
                return result

        # we have run out of items, compare lengths
        length_left = len(left)
        length_right = len(right)

        if length_left == length_right:
            return None

        if length_right > length_left:
            return True

        return False

    # Unequal types
    indent += INDENT_CHAR

    if type_left is int:
        logger.debug(
            f"{indent}- Mixed types; convert left to [{left}] and retry comparison"
        )
        return are_in_order([left], right, level + 1)

    # right should be an int
    logger.debug(
        f"{indent}- Mixed types; convert right to [{right}] and retry comparison"
    )
    return are_in_order(left, [right], level + 1)


def bubble_sort(items):

    swapped = False
    # Looping from size of array from last index[-1] to index [0]
    for end in range(len(items) - 1, 0, -1):
        for i in range(end):
            if not are_in_order(items[i], items[i + 1]):
                swapped = True
                # swap in-place
                items[i], items[i + 1] = items[i + 1], items[i]
        # optimization, return when already sorted
        if not swapped:
            return


def merge_sort(items):

    if len(items) <= 1:
        return

    # find midpoint
    mid = len(items) // 2

    # split in two halfs
    L, R = items[:mid], items[mid:]

    # sort the left and right half
    merge_sort(L)
    merge_sort(R)

    i = j = k = 0

    # Copy data to temp arrays L[] and R[]
    while i < len(L) and j < len(R):
        if are_in_order(L[i], R[j]):
            items[k] = L[i]
            i += 1
        else:
            items[k] = R[j]
            j += 1
        k += 1

    # Checking if any element was left
    while i < len(L):
        items[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        items[k] = R[j]
        j += 1
        k += 1


def solve_part_one(lines):
    packet_pair_index = 1

    packet_pairs_results = {True: [], False: []}

    for first_packet, second_packet in parse_handheld_packets(lines):

        logger.debug(f"== Pair {packet_pair_index} ==")

        result = are_in_order(first_packet, second_packet)

        packet_pairs_results[result].append(packet_pair_index)

        packet_pair_index += 1

    return sum(packet_pairs_results[True])


def solve_part_two(lines):
    packets = []
    for first, second in parse_handheld_packets(lines):
        packets.extend([first, second])
    divider_packets = [[[2]], [[6]]]
    packets.extend(divider_packets)

    # bubble_sort(packets)
    merge_sort(packets)
    # packets = sorted(packets, key=functools.cmp_to_key(are_in_order))

    for packet in packets:
        logger.debug(packet)

    return (packets.index(divider_packets[0]) + 1) * (
        packets.index(divider_packets[1]) + 1
    )
