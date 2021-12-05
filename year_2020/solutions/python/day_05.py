import os
from typing import List, Callable

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER


def find_seat(seats: List[str], search_function: Callable[[List[str]], int]) -> int:
    return search_function(seats)


def get_missing_id(seats: List[str]) -> int:
    ordered_seat_ids: List[int] = sorted((compute_seat_id(seat) for seat in seats))
    for i in range(len(ordered_seat_ids)):
        if ordered_seat_ids[i + 1] - ordered_seat_ids[i] == 2:
            return ordered_seat_ids[i] + 1


def get_max_id(seats: List[str]) -> int:
    return max((compute_seat_id(seat) for seat in seats))


def compute_seat_id(seat: str) -> int:
    return get_row(seat) * 8 + get_column(seat)


def get_row(seat: str) -> int:
    row_binary: str = seat[:-3].replace('F', '0').replace('B', '1')
    return int(row_binary, base=2)


def get_column(seat: str) -> int:
    column_binary: str = seat[-3:].replace('L', '0').replace('R', '1')
    return int(column_binary, base=2)


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_05', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = find_seat(seats=input_list, search_function=get_max_id)
    assert part_1_result == 953
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = find_seat(seats=input_list, search_function=get_missing_id)
    assert part_2_result == 615
    print('Part 2 result :', part_2_result)
