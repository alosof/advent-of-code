from typing import List, Dict, Optional


def get_last_spoken_number(starting_sequence: List[int], turns_to_play: int) -> int:
    game_memory: Dict[int, int] = {v: k + 1 for k, v in enumerate(starting_sequence)}
    turn: int = len(starting_sequence) + 1
    spoken_number: int = 0
    while turn < turns_to_play:
        previous_time: Optional[int] = game_memory.get(spoken_number, None)
        game_memory[spoken_number] = turn
        spoken_number = 0 if previous_time is None else turn - previous_time
        turn += 1

    return spoken_number


if __name__ == '__main__':
    input_list: List[int] = [9, 19, 1, 6, 0, 5, 4]

    # Part 1
    part_1_result: int = get_last_spoken_number(starting_sequence=input_list, turns_to_play=2020)
    assert part_1_result == 1522
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = get_last_spoken_number(starting_sequence=input_list, turns_to_play=30000000)
    assert part_2_result == 18234
    print('Part 2 result :', part_2_result)
