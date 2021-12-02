import os
from functools import reduce
from typing import List, Callable, Set, Generator

from year_2020.solutions.python.utils.files import read_list_of_lists, INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def count_answers(groups: List[List[str]], count_method: Callable[[List[str]], Set[str]]) -> int:
    return sum((len(count_method(group)) for group in groups))


def answered_by_anyone_in_group(group: List[str]) -> Set[str]:
    unique_answers: Generator[Set[str], None, None] = (set(individual_answers) for individual_answers in group)
    return reduce(lambda x, y: x.union(y), unique_answers)


def answered_by_everyone_in_group(group: List[str]) -> Set[str]:
    unique_answers: Generator[Set[str], None, None] = (set(individual_answers) for individual_answers in group)
    return reduce(lambda x, y: x.intersection(y), unique_answers)


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_06', 'input.txt')
    input_list: List[List[str]] = read_list_of_lists(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = count_answers(groups=input_list, count_method=answered_by_anyone_in_group)
    assert part_1_result == 6585
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_answers(groups=input_list, count_method=answered_by_everyone_in_group)
    assert part_2_result == 3276
    print('Part 2 result :', part_2_result)
