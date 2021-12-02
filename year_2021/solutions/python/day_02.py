from typing import List
from pathlib import Path
from year_2021.solutions.python.utils.files import read_lines, INPUTS_FOLDER


def move_with_simple_commands(instructions_list: List[str]) -> int:
    position, depth = 0, 0
    for instruction in instructions_list:
        match instruction.split():
            case ['forward', value]:
                position += int(value)
            case ['down', value]:
                depth += int(value)
            case ['up', value]:
                depth -= int(value)
    return position * depth


def move_with_advanced_commands(instructions_list: List[str]) -> int:
    position, depth, aim = 0, 0, 0
    for instruction in instructions_list:
        match instruction.split():
            case ['forward', value]:
                position += int(value)
                depth += aim * int(value)
            case ['down', value]:
                aim += int(value)
            case ['up', value]:
                aim -= int(value)
    return position * depth


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    instructions: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = move_with_simple_commands(instructions)
    assert part_1_result == 1459206
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = move_with_advanced_commands(instructions)
    assert part_2_result == 1320534480
    print('Part 2 result :', part_2_result)
