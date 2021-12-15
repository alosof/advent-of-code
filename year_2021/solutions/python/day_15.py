from pathlib import Path
from typing import List, Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_int_grid


def safest_path_total_risk(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    lowest_risk_by_destination = {}
    total_risk = 0
    search_space = [(total_risk, 0, 0)]
    while len(search_space) > 0:
        search_space = sorted(search_space, key=lambda e: e[0])
        total_risk, i, j = search_space.pop(0)
        if (i, j) in lowest_risk_by_destination and lowest_risk_by_destination[(i, j)] <= total_risk:
            continue
        else:
            lowest_risk_by_destination[(i, j)] = total_risk
            if (i, j) == (rows - 1, cols - 1):
                return lowest_risk_by_destination[(i, j)]
            for n_i, n_j in neighbors((i, j), grid):
                search_space.append((total_risk + grid[n_i][n_j], n_i, n_j))


def in_bounds(candidate: Tuple[int, int], grid: List[List[int]]) -> bool:
    return (0 <= candidate[0] < len(grid)) and (0 <= candidate[1] < len(grid[0]))


def neighbors(p: Tuple[int, int], grid: List[List[int]]) -> List[Tuple[int, int]]:
    offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    candidates = [(p[0] + o[0], p[1] + o[1]) for o in offsets]
    return [c for c in candidates if in_bounds(c, grid)]


def expand_grid(grid: List[List[int]]) -> List[List[int]]:
    expanded_grid = [[0 for _ in range(len(grid[0]) * 5)] for _ in range(len(grid) * 5)]
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    expanded_grid_rows = len(expanded_grid)
    expanded_grid_cols = len(expanded_grid[0])
    blocks = build_expanded_grid_blocks(grid)
    for i in range(expanded_grid_rows):
        for j in range(expanded_grid_cols):
            block = blocks[i // grid_rows][j // grid_cols]
            b_i, b_j = i % grid_rows, j % grid_cols
            expanded_grid[i][j] = block[b_i][b_j]
    return expanded_grid


def build_expanded_grid_blocks(grid: List[List[int]]) -> List[List[List[List[int]]]]:
    blocks = [[[] for _ in range(5)] for _ in range(5)]
    blocks[0][0] = grid
    for i in range(5):
        for j in range(5):
            blocks[i][j] = increment(grid, times=manhattan_distance((0, 0), (i, j)))
    return blocks


def increment(grid: List[List[int]], times: int = 1) -> List[List[int]]:
    res = grid
    for i in range(times):
        res = [[res[i][j] + 1 if res[i][j] < 9 else 1 for j in range(len(res[0]))] for i in range(len(res))]
    return res


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    input_grid: List[List[int]] = read_int_grid(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = safest_path_total_risk(input_grid)
    assert part_1_result == 741
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = safest_path_total_risk(expand_grid(input_grid))
    assert part_2_result == 2976
    print('Part 2 result :', part_2_result)
