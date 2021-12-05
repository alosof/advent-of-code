import os
from typing import List, Tuple

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER


def evaluate_accumulator(instructions_list: List[str], fix_program: bool) -> int:
    if fix_program:
        return evaluate_accumulator_when_program_is_fixed(instructions_list)
    else:
        return evaluate_accumulator_and_termination(instructions_list)[0]


def evaluate_accumulator_when_program_is_fixed(instructions_list: List[str]) -> int:
    for i in range(len(instructions_list)):
        accumulator, terminated = evaluate_accumulator_and_termination(switch_instruction(i, instructions_list))
        if terminated:
            return accumulator


def switch_instruction(i: int, instructions_list: List[str]) -> List[str]:
    new_instructions: List[str] = input_list.copy()
    if instructions_list[i].startswith('nop'):
        new_instructions[i] = new_instructions[i].replace('nop', 'jmp')
    elif instructions_list[i].startswith('jmp'):
        new_instructions[i] = new_instructions[i].replace('jmp', 'nop')
    return new_instructions


def evaluate_accumulator_and_termination(instructions_list: List[str]) -> Tuple[int, bool]:
    accumulator: int = 0
    visited = set()
    i = 0
    terminated: bool = False
    while i not in visited:
        terminated = i == len(instructions_list)
        if terminated:
            return accumulator, terminated
        visited.add(i)
        instruction, value = instructions_list[i].split()
        if instruction == 'nop':
            i += 1
        elif instruction == 'acc':
            accumulator += int(value)
            i += 1
        elif instruction == 'jmp':
            i += int(value)
        else:
            raise ValueError('Invalid instruction')
    return accumulator, terminated


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_08', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = evaluate_accumulator(input_list, fix_program=False)
    assert part_1_result == 1915
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = evaluate_accumulator(input_list, fix_program=True)
    assert part_2_result == 944
    print('Part 2 result :', part_2_result)
