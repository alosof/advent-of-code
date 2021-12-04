from pathlib import Path
from typing import List, Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_int_grid


def compute_power_consumption(report: List[List[int]]) -> int:
    return gamma_rate(report) * epsilon_rate(report)


def compute_life_support_rating(report: List[List[int]]) -> int:
    return oxygen_rating(report) * co2_rating(report)


def gamma_rate(report: List[List[int]]) -> int:
    return to_decimal([most_common(report, c) for c in range(len(report[0]))])


def epsilon_rate(report: List[List[int]]) -> int:
    return to_decimal([least_common(report, c) for c in range(len(report[0]))])


def oxygen_rating(report: List[List[int]]) -> int:
    oxygen_report = report.copy()
    c = 0
    while len(oxygen_report) > 1 and c < len(oxygen_report[0]):
        oxygen_report = [row for row in oxygen_report if row[c] == most_common(oxygen_report, c)]
        c += 1
    return to_decimal(oxygen_report[0])


def co2_rating(report: List[List[int]]) -> int:
    co2_report = report.copy()
    c = 0
    while len(co2_report) > 1 and c < len(co2_report[0]):
        co2_report = [row for row in co2_report if row[c] == least_common(co2_report, c)]
        c += 1
    return to_decimal(co2_report[0])


def most_common(report: List[List[int]], column: int):
    zeros, ones = count_zeros_and_ones(report, column)
    return 0 if zeros > ones else 1


def least_common(report: List[List[int]], column: int):
    zeros, ones = count_zeros_and_ones(report, column)
    return 1 if ones < zeros else 0


def count_zeros_and_ones(report: List[List[int]], column: int) -> Tuple[int, int]:
    selected_column = select_column(report, column)
    zeros = sum([e == 0 for e in selected_column])
    ones = sum([e == 1 for e in selected_column])
    return zeros, ones


def to_decimal(bits: List[int]) -> int:
    return int(''.join([str(b) for b in bits]), base=2)


def select_column(report: List[List[int]], column: int) -> List[int]:
    return [row[column] for row in report]


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    diagnostic_report: List[List[int]] = read_int_grid(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = compute_power_consumption(diagnostic_report)
    assert part_1_result == 3309596
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = compute_life_support_rating(diagnostic_report)
    assert part_2_result == 2981085
    print('Part 2 result :', part_2_result)
