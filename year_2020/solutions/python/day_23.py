from typing import List, Dict


def multiply_the_two_successors_of_cup_one(starting_config: int, total_cups: int, moves: int) -> int:
    cups_linked_list: Dict[int, int] = move_cups(starting_config, total_cups, moves)
    return cups_linked_list[1] * cups_linked_list[cups_linked_list[1]]


def list_labels_after_cup_one(starting_config: int, total_cups: int, moves: int) -> int:
    cups_linked_list: Dict[int, int] = move_cups(starting_config, total_cups, moves)
    result: str = ''
    cup: int = 1
    for _ in range(len(cups_linked_list) - 1):
        n = cups_linked_list[cup]
        result += str(n)
        cup = n
    return int(result)


def move_cups(starting_config: int, total_cups: int, moves: int) -> Dict[int, int]:
    cups: List[int] = list_all_cups(starting_config, total_cups)
    total_cups: int = len(cups)
    cups_linked_list: Dict[int, int] = {cups[i]: cups[(i + 1) % total_cups] for i in range(total_cups)}
    current_cup: int = cups[0]
    for move in range(1, moves + 1):
        picked_up_1: int = cups_linked_list[current_cup]
        picked_up_2: int = cups_linked_list[picked_up_1]
        picked_up_3: int = cups_linked_list[picked_up_2]

        next_current_cup: int = cups_linked_list[picked_up_3]

        destination_cup: int = get_destination_cup(current_cup, total_cups, [picked_up_1, picked_up_2, picked_up_3])
        buffer: int = cups_linked_list[destination_cup]
        cups_linked_list[destination_cup] = picked_up_1
        cups_linked_list[picked_up_3] = buffer

        cups_linked_list[current_cup] = next_current_cup
        current_cup = next_current_cup

    return cups_linked_list


def get_destination_cup(curr: int, number_of_cups: int, picked_up: List[int]) -> int:
    dest: int = curr - 1
    if dest == 0:
        dest = number_of_cups
    while dest in picked_up:
        dest = dest - 1
        if dest == 0:
            dest = number_of_cups
    return dest


def list_all_cups(starting_config: int, total_cups: int) -> List[int]:
    starting_conf_as_list: List[int] = list(map(int, str(starting_config)))
    return starting_conf_as_list + list(range(max(starting_conf_as_list) + 1, total_cups + 1))


if __name__ == '__main__':
    start_config: int = 253149867

    # Part 1
    part_1_result: int = list_labels_after_cup_one(starting_config=start_config,
                                                   total_cups=9,
                                                   moves=100)
    assert part_1_result == 34952786
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = multiply_the_two_successors_of_cup_one(starting_config=start_config,
                                                                total_cups=1000000,
                                                                moves=10000000)
    assert part_2_result == 505334281774
    print('Part 2 result :', part_2_result)
