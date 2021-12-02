import os
from typing import List, Tuple

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def navigation_distance(raw_instructions: List[str], method: str) -> int:
    instructions: List[Tuple[str, int]] = [parse_instruction(i) for i in raw_instructions]
    final_ship_position: Tuple[int, int] = navigate(instructions, method)
    return manhattan_distance_from_origin(final_ship_position)


def navigate(instructions: List[Tuple[str, int]], method: str) -> Tuple[int, int]:
    ship_pos = 0, 0
    if method == 'simple':
        ship_dir = 'E'
        for instruction in instructions:
            ship_pos, ship_dir = move_simple(ship_pos, ship_dir, instruction)
        return ship_pos
    elif method == 'waypoint':
        waypoint_relative_pos = 10, 1
        for instruction in instructions:
            ship_pos, waypoint_relative_pos = move_with_waypoint(ship_pos, waypoint_relative_pos, instruction)
        return ship_pos
    else:
        raise ValueError('Invalid navigation method')


def manhattan_distance_from_origin(position: Tuple[int, int]) -> int:
    return abs(position[0]) + abs(position[1])


def move_simple(ship_pos: Tuple[int, int], ship_dir: str, instruction: Tuple[str, int]) -> Tuple[Tuple[int, int], str]:
    offsets = {
        'E': (1, 0),
        'W': (-1, 0),
        'N': (0, 1),
        'S': (0, -1),
    }
    current_x, current_y = ship_pos
    direction, value = instruction
    if direction in ('E', 'W', 'N', 'S'):
        new_pos = current_x + offsets[direction][0] * value, current_y + offsets[direction][1] * value
        return new_pos, ship_dir
    elif direction in ('R', 'L'):
        ordered_dirs: List[str] = ['E', 'S', 'W', 'N']
        rotation_dir: int = 1 if direction == 'R' else -1
        new_ship_dir_idx = (ordered_dirs.index(ship_dir) + rotation_dir * (value // 90)) % 4
        new_dir = ordered_dirs[new_ship_dir_idx]
        return ship_pos, new_dir
    elif direction == 'F':
        new_instruction = ship_dir, value
        return move_simple(ship_pos, ship_dir, new_instruction)


def move_with_waypoint(ship_pos: Tuple[int, int], waypoint_relative_pos: Tuple[int, int], instruction: Tuple[str, int]):
    direction, value = instruction
    if direction in ('E', 'W', 'N', 'S'):
        new_waypoint_relative_pos, _ = move_simple(waypoint_relative_pos, direction, instruction)
        return ship_pos, new_waypoint_relative_pos
    if direction in ('R', 'L'):
        new_waypoint_relative_pos = rotate_waypoint(waypoint_relative_pos, direction, value)
        return ship_pos, new_waypoint_relative_pos
    if direction == 'F':
        new_ship_pos = ship_pos[0] + value * waypoint_relative_pos[0], ship_pos[1] + value * waypoint_relative_pos[1]
        return new_ship_pos, waypoint_relative_pos


def rotate_waypoint(waypoint_relative_pos: Tuple[int, int], direction: str, angle: int) -> Tuple[int, int]:
    clockwise_quarter_turns = count_clockwise_quarter_turns(direction, angle)
    if clockwise_quarter_turns == 0:
        return waypoint_relative_pos[0], waypoint_relative_pos[1]
    elif clockwise_quarter_turns == 1:
        return waypoint_relative_pos[1], -waypoint_relative_pos[0]
    elif clockwise_quarter_turns == 2:
        return -waypoint_relative_pos[0], -waypoint_relative_pos[1]
    elif clockwise_quarter_turns == 3:
        return -waypoint_relative_pos[1], waypoint_relative_pos[0]


def count_clockwise_quarter_turns(direction: str, angle: int) -> int:
    if direction == 'R':
        return (angle // 90) % 4
    elif direction == 'L':
        return 4 - (angle // 90) % 4
    else:
        raise ValueError(f'Invalid direction for rotation : {direction}')


def parse_instruction(instruction) -> Tuple[str, int]:
    return instruction[0], int(instruction[1:])


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_12', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = navigation_distance(input_list, 'simple')
    assert part_1_result == 1601
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = navigation_distance(input_list, 'waypoint')
    assert part_2_result == 13340
    print('Part 2 result :', part_2_result)
