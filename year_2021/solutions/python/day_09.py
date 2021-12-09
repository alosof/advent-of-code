from dataclasses import dataclass
from functools import reduce
from math import prod
from pathlib import Path
from typing import List, Set

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_int_grid


@dataclass(frozen=True)
class Point:
    row: int
    col: int


def compute_product_of_three_largest_basins_sizes(heightmap: List[List[int]]) -> int:
    low_points = find_low_points(heightmap)
    basins = {point: get_basin_around_point(point, heightmap, set()) for point in low_points}
    sizes = {low_point: len(basin_points) for low_point, basin_points in basins.items()}
    return prod(sorted(sizes.values())[-3:])


def get_basin_around_point(point: Point, heightmap: List[List[int]], visited: Set[Point]) -> Set[Point]:
    rows = len(heightmap)
    cols = len(heightmap[0])
    if point in visited or height(point, heightmap) == 9:
        return set()
    else:
        visited.add(point)
        neighbors = get_neighbors(point=point, max_row=rows, max_col=cols)
        return {point}.union(
            reduce(set.union, [get_basin_around_point(neighbor, heightmap, visited) for neighbor in neighbors])
        )


def compute_low_points_risk(heightmap: List[List[int]]) -> int:
    return sum((height(point, heightmap) + 1 for point in find_low_points(heightmap)))


def find_low_points(heightmap: List[List[int]]) -> Set[Point]:
    rows = len(heightmap)
    cols = len(heightmap[0])
    low_points = set()
    for row in range(rows):
        for col in range(cols):
            point = Point(row, col)
            neighbors = get_neighbors(point=point, max_row=rows, max_col=cols)
            if all([height(point, heightmap) < height(neighbor, heightmap) for neighbor in neighbors]):
                low_points.add(point)
    return low_points


def get_neighbors(point: Point, max_row: int, max_col: int) -> List[Point]:
    up = Point(point.row - 1, point.col) if point.row > 0 else None
    down = Point(point.row + 1, point.col) if (point.row + 1) < max_row else None
    left = Point(point.row, point.col - 1) if point.col > 0 else None
    right = Point(point.row, point.col + 1) if (point.col + 1) < max_col else None
    return [neighbor for neighbor in [up, down, left, right] if neighbor is not None]


def height(point: Point, heightmap: List[List[int]]) -> int:
    return heightmap[point.row][point.col]


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    height_map: List[List[int]] = read_int_grid(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = compute_low_points_risk(heightmap=height_map)
    assert part_1_result == 508
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = compute_product_of_three_largest_basins_sizes(heightmap=height_map)
    assert part_2_result == 1564640
    print('Part 2 result :', part_2_result)
