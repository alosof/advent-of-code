import os
from math import prod
from typing import List, Tuple

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def multiply_tree_counts_for_several_slopes(area_map: List[str], slopes: List[Tuple[int, int]]) -> int:
    return prod(count_trees(area_map, slope_right, slope_down) for slope_right, slope_down in slopes)


def count_trees(area_map: List[str], slope_right: int, slope_down: int) -> int:
    map_bottom_row = len(area_map)
    map_rightmost_column = len(area_map[0])
    row, column, tree_count = 0, 0, 0
    while row < map_bottom_row:
        if area_map[row][column] == '#':
            tree_count += 1
        row += slope_down
        column = (column + slope_right) % map_rightmost_column
    return tree_count


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_03', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = multiply_tree_counts_for_several_slopes(area_map=input_list, slopes=[(3, 1)])
    assert part_1_result == 211
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = multiply_tree_counts_for_several_slopes(area_map=input_list,
                                                                 slopes=[(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
    assert part_2_result == 3584591857
    print('Part 2 result :', part_2_result)
