import os
from copy import deepcopy
from itertools import product
from typing import List, Dict, Tuple, Callable

from year_2020.solutions.python.utils.files import read_grid, INPUTS_FOLDER

Map = List[List[str]]

DIRECTIONS: Dict[str, Tuple[int, int]] = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1),
    'UP_LEFT': (-1, -1),
    'UP_RIGHT': (-1, 1),
    'DOWN_LEFT': (1, -1),
    'DOWN_RIGHT': (1, 1)
}


def count_neighbors_after_map_stabilizes(seat_map: Map,
                                         threshold: int,
                                         neighbor_counter: Callable[[int, int, Map], int]) -> int:
    updated_seat_map = None
    while updated_seat_map != seat_map:
        updated_seat_map = seat_map
        seat_map = update_seat_map(seat_map, threshold, neighbor_counter)
    return count_all_occupied_seats(seat_map)


def update_seat_map(seat_map: Map, tolerance_threshold: int, neighbor_counter: Callable[[int, int, Map], int]) -> Map:
    new_seat_map: Map = deepcopy(seat_map)
    rows = len(seat_map)
    cols = len(seat_map[0])
    for row, col in product(range(rows), range(cols)):
        if seat_map[row][col] == 'L' and neighbor_counter(row, col, seat_map) == 0:
            new_seat_map[row][col] = '#'
        elif seat_map[row][col] == '#' and neighbor_counter(row, col, seat_map) >= tolerance_threshold:
            new_seat_map[row][col] = 'L'
    return new_seat_map


def count_adjacent_neighbors(row: int, col: int, seat_map: Map) -> int:
    rows = len(seat_map)
    cols = len(seat_map[0])
    occupied = 0
    for row_offset, col_offset in DIRECTIONS.values():
        neighbor_row: int = row + row_offset
        neighbor_col: int = col + col_offset
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and seat_map[neighbor_row][neighbor_col] == '#':
            occupied += 1
    return occupied


def count_nearest_neighbors(row: int, col: int, seat_map: Map) -> int:
    rows = len(seat_map)
    cols = len(seat_map[0])
    occupied = 0
    for row_offset, col_offset in DIRECTIONS.values():
        neighbor_row: int = row + row_offset
        neighbor_col: int = col + col_offset
        while 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            if seat_map[neighbor_row][neighbor_col] == 'L':
                break
            if seat_map[neighbor_row][neighbor_col] == '#':
                occupied += 1
                break
            neighbor_row += row_offset
            neighbor_col += col_offset
    return occupied


def count_all_occupied_seats(seat_map: Map) -> int:
    rows = len(seat_map)
    cols = len(seat_map[0])
    return sum((seat_map[row][col] == '#' for row, col in product(range(rows), range(cols))))


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_11', 'input.txt')
    input_list: Map = read_grid(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = count_neighbors_after_map_stabilizes(seat_map=input_list,
                                                              threshold=4,
                                                              neighbor_counter=count_adjacent_neighbors)
    assert part_1_result == 2386
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_neighbors_after_map_stabilizes(seat_map=input_list,
                                                              threshold=5,
                                                              neighbor_counter=count_nearest_neighbors)
    assert part_2_result == 2091
    print('Part 2 result :', part_2_result)
