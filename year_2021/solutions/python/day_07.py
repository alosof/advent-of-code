from pathlib import Path
from typing import List, Callable

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_int_line


def fuel_to_reach_optimal_position(positions: List[int], fuel_consumption: Callable[[int, int], int]) -> int:
    return min(sum(fuel_consumption(ref_crab, crab) for crab in positions) for ref_crab in positions)


def linear_fuel_consumption(ref_crab: int, crab: int) -> int:
    return abs(crab - ref_crab)


def quadratic_fuel_consumption(ref_crab: int, crab: int) -> int:
    abs_dist = abs(crab - ref_crab)
    return abs_dist * (abs_dist + 1) // 2


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    crab_positions: List[int] = read_int_line(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = fuel_to_reach_optimal_position(crab_positions, linear_fuel_consumption)
    assert part_1_result == 344138
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = fuel_to_reach_optimal_position(crab_positions, quadratic_fuel_consumption)
    assert part_2_result == 94862124
    print('Part 2 result :', part_2_result)
