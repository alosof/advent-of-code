import os
from typing import List, Dict, Tuple

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def count_valid_arrangements(joltages: List[int]) -> int:
    sorted_joltages: List[int] = sort_joltages_including_outlet_and_device(joltages)
    return count_valid_arrangements_of_sorted_joltages(sorted_joltages, memory={})


def count_valid_arrangements_of_sorted_joltages(sorted_joltages: List[int], memory: Dict[Tuple[int], int]) -> int:
    sorted_joltages_key: Tuple[int] = tuple(sorted_joltages)
    if len(sorted_joltages) == 1:
        valid_arrangements = 1
    elif sorted_joltages_key in memory:
        valid_arrangements = memory[sorted_joltages_key]
    else:
        valid_arrangements = sum((count_valid_arrangements_of_sorted_joltages(sorted_joltages[successor:], memory)
                                  for successor in valid_successors_indices(0, sorted_joltages)))
    memory[sorted_joltages_key] = valid_arrangements
    return valid_arrangements


def valid_successors_indices(reference_adapter_idx: int, sorted_joltages: List[int]) -> List[int]:
    candidate_adapters_indices = range(reference_adapter_idx + 1, min(reference_adapter_idx + 4, len(sorted_joltages)))
    return [candidate_adapter_idx for candidate_adapter_idx in candidate_adapters_indices
            if is_valid_transition(reference_adapter_idx, candidate_adapter_idx, sorted_joltages)]


def is_valid_transition(reference_adapter_idx: int, candidate_adapter_idx: int, joltages: List[int]) -> bool:
    return 1 <= joltages[candidate_adapter_idx] - joltages[reference_adapter_idx] <= 3


@timer
def compute_joltage_differences_distribution(joltages: List[int]) -> int:
    sorted_joltages: List[int] = sort_joltages_including_outlet_and_device(joltages)
    jumps = [a - b for a, b in zip(sorted_joltages[1:], sorted_joltages[:-1])]
    return sum([int(e == 3) for e in jumps]) * sum([int(e == 1) for e in jumps])


def sort_joltages_including_outlet_and_device(joltages: List[int]) -> List[int]:
    sorted_joltages: List[int] = sorted(joltages)
    outlet_joltage: int = 0
    device_adapter_joltage: int = sorted_joltages[-1] + 3
    return [outlet_joltage] + sorted_joltages + [device_adapter_joltage]


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_10', 'input.txt')
    input_list: List[int] = read_lines(input_file_path=input_file_path, line_type=int)

    # Part 1
    part_1_result: int = compute_joltage_differences_distribution(input_list)
    assert part_1_result == 2664
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_valid_arrangements(input_list)
    assert part_2_result == 148098383347712
    print('Part 2 result :', part_2_result)
