import os
from typing import List, Tuple, Callable

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def count_valid_passwords(input_sequence: List[str], check_function: Callable[[str, str, int, int], bool]) -> int:
    return sum(check_function(*split_line(line)) for line in input_sequence)


def split_line(line: str) -> Tuple[str, str, int, int]:
    positions, letter_with_colon, password = line.split(' ')
    low_position, high_position = [int(pos) for pos in positions.split('-')]
    control_letter = letter_with_colon[:-1]
    return password, control_letter, low_position, high_position


def check_validity_old_policy(password: str, control_letter: str, low_position: int, high_position: int) -> bool:
    return low_position <= password.count(control_letter) <= high_position


def check_validity_new_policy(password: str, control_letter: str, low_position: int, high_position: int) -> bool:
    return (password[low_position - 1] == control_letter) != (password[high_position - 1] == control_letter)


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_02', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = count_valid_passwords(input_sequence=input_list, check_function=check_validity_old_policy)
    assert part_1_result == 506
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_valid_passwords(input_sequence=input_list, check_function=check_validity_new_policy)
    assert part_2_result == 443
    print('Part 2 result :', part_2_result)
