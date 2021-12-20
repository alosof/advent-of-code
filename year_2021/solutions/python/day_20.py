from pathlib import Path
from typing import List, Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines



def read_algorithm_and_image() -> Tuple[List[str], List[List[str]]]:
    pass


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    snail_numbers: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = total_sum_magnitude(snail_numbers)
    assert part_1_result == 3675
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result = highest_pair_magnitude(snail_numbers)
    assert part_2_result == 4650
    print('Part 2 result :', part_2_result)
