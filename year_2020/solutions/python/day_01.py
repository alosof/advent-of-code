import os
from functools import reduce
from itertools import combinations
from operator import mul
from typing import List

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER


def process_expense_report(input_sequence: List[int], tuple_size: int, expected_sum: int) -> int:
    return compute_product(find_tuple(input_sequence=input_sequence, tuple_size=tuple_size, expected_sum=expected_sum))


def compute_product(found_tuple: tuple) -> int:
    return reduce(mul, found_tuple)


def find_tuple(input_sequence: List[int], tuple_size: int, expected_sum: int) -> tuple:
    sorted_input = sorted(input_sequence)
    for combination in combinations(sorted_input, tuple_size):
        if sum(combination) == expected_sum:
            return combination


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_01', 'input.txt')
    input_list: List[int] = read_lines(input_file_path=input_file_path, line_type=int)

    # Part 1
    part_1_result: int = process_expense_report(input_sequence=input_list, tuple_size=2, expected_sum=2020)
    assert part_1_result == 270144
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = process_expense_report(input_sequence=input_list, tuple_size=3, expected_sum=2020)
    assert part_2_result == 261342720
    print('Part 2 result :', part_2_result)
