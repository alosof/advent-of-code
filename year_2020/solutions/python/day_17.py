import os
from itertools import product
from typing import Set, List, Dict
from typing import Tuple

from year_2020.solutions.python.utils.files import INPUTS_FOLDER, read_lines
from year_2020.solutions.python.utils.timing import timer

Point = Tuple[int, ...]
SparseMap = Set[Point]


@timer
def count_active_cubes_after_cycles(lines: List[str], dimensions: int, cycles: int) -> int:
    sparse_map: SparseMap = build_sparse_map_of_active_points(lines, dimensions)
    for c in range(1, cycles + 1):
        sparse_map = cycle(sparse_map)
    return len(sparse_map)


def cycle(sparse_map: SparseMap) -> SparseMap:
    next_map: SparseMap = set()
    non_isolated_points_active_neighbors: Dict[Point, int] = count_active_neighbors_of_non_isolated_points(sparse_map)
    for point in non_isolated_points_active_neighbors:
        if becomes_active(point, sparse_map, non_isolated_points_active_neighbors):
            next_map.add(point)
    return next_map


def becomes_active(point: Point, sparse_map: SparseMap, active_neighbors: Dict[Point, int]) -> bool:
    return (point in sparse_map and active_neighbors[point] in (2, 3)) or \
           (point not in sparse_map and active_neighbors[point] == 3)


def count_active_neighbors_of_non_isolated_points(sparse_map: SparseMap) -> Dict[Point, int]:
    non_isolated_points_active_neighbors: Dict[Point, int] = {}
    for point in sparse_map:
        for neighbor in neighbors(point):
            non_isolated_points_active_neighbors[neighbor] = non_isolated_points_active_neighbors.get(neighbor, 0) + 1
    return non_isolated_points_active_neighbors


def neighbors(point: Point) -> Set[Point]:
    return set(tuple(map(sum, zip(point, offset))) for offset in offsets(dimension=len(point)))


def offsets(dimension: int) -> Set[Tuple[int, ...]]:
    return set(product(*(range(-1, 2) for _ in range(dimension)))).difference([(0,) * dimension])


def build_sparse_map_of_active_points(lines: List[str], dimensions: int) -> SparseMap:
    return set((row, column) + (0,) * (dimensions - 2)
               for row, column in product(range(len(lines)), range(len(lines[0])))
               if lines[row][column] == '#')


def draw_active_part_of_3d_universe(sparse_map: SparseMap) -> None:
    row_min, row_max = min(p[0] for p in sparse_map), max(p[0] for p in sparse_map)
    col_min, col_max = min(p[1] for p in sparse_map), max(p[1] for p in sparse_map)
    height_min, height_max = min(p[2] for p in sparse_map), max(p[2] for p in sparse_map)
    complete_map = [[['.'
                      for _ in range(col_min, col_max + 1)]
                     for _ in range(row_min, row_max + 1)]
                    for _ in range(height_min, height_max + 1)]
    for point in sparse_map:
        complete_map[point[2] - height_min][point[0] - row_min][point[1] - col_min] = '#'

    for plane_idx, plane in enumerate(complete_map):
        print(f'z={plane_idx + height_min}')
        for row in plane:
            print(''.join(row))
        print('\n')


if __name__ == "__main__":
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_17', 'input.txt')
    input_lines: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = count_active_cubes_after_cycles(lines=input_lines, dimensions=3, cycles=6)
    assert part_1_result == 223
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_active_cubes_after_cycles(lines=input_lines, dimensions=4, cycles=6)
    assert part_2_result == 1884
    print('Part 2 result :', part_2_result)
