from typing import List
from pathlib import Path
from year_2021.solutions.python.utils.files import read_lines, INPUTS_FOLDER


def count_measurement_increases(measurements_report: List[int]) -> int:
    return sum((b - a > 0 for (b, a) in zip(measurements_report[1:], measurements_report[:-1])))


def compute_size_three_window_sums(measurements_report: List[int]) -> List[int]:
    return [sum(measurements_report[i:(i + 3)]) for i in range(len(measurements_report) - 2)]


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    measurements: List[int] = read_lines(input_file_path=input_file_path, line_type=int)

    # Part 1
    part_1_result: int = count_measurement_increases(measurements)
    assert part_1_result == 1521
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_measurement_increases(compute_size_three_window_sums(measurements))
    assert part_2_result == 1543
    print('Part 2 result :', part_2_result)
