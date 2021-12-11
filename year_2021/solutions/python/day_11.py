from itertools import product
from pathlib import Path
from typing import List, Tuple, Set

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_int_grid


def count_flashes(grid: List[List[int]], steps: int) -> int:
    previous_grid = grid.copy()
    flashes = 0
    for i in range(steps):
        step_flashes, grid_after_step = step(previous_grid)
        flashes += step_flashes
        previous_grid = grid_after_step
    return flashes


def first_synchronized_flash(grid: List[List[int]]) -> int:
    grid_area = len(grid) * len(grid[0])
    previous_grid = grid.copy()
    _step = 0
    while True:
        _step += 1
        step_flashes, grid_after_step = step(previous_grid)
        if step_flashes == grid_area:
            return _step
        previous_grid = grid_after_step


def step(grid: List[List[int]]) -> Tuple[int, List[List[int]]]:
    new_grid = grid.copy()
    flashed = set()
    new_grid = charge(new_grid)
    octopuses_to_flash = locate_octopuses_to_flash(new_grid, flashed)
    while len(octopuses_to_flash) > 0:
        for octopus in octopuses_to_flash:
            new_grid = propagate_around(octopus, new_grid)
        flashed = flashed.union(octopuses_to_flash)
        octopuses_to_flash = locate_octopuses_to_flash(new_grid, flashed)
    return len(flashed), discharge(new_grid)


def locate_octopuses_to_flash(grid: List[List[int]], already_flashed: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    octopuses_to_flash = set()
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c > 9 and (i, j) not in already_flashed:
                octopuses_to_flash.add((i, j))
    return octopuses_to_flash


def propagate_around(octopus: Tuple[int, int], grid: List[List[int]]) -> List[List[int]]:
    new_grid = grid.copy()
    offsets = [o for o in product(range(-1, 2), range(-1, 2)) if o != (0, 0)]
    for o in offsets:
        neighbor_i = octopus[0] + o[0]
        neighbor_j = octopus[1] + o[1]
        if is_in_bounds((neighbor_i, neighbor_j), grid):
            new_grid[neighbor_i][neighbor_j] = new_grid[neighbor_i][neighbor_j] + 1
    return new_grid


def is_in_bounds(neighbor: Tuple[int, int], grid: List[List[int]]) -> bool:
    rows = len(grid)
    cols = len(grid[0])
    return 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols


def charge(grid: List[List[int]]) -> List[List[int]]:
    return [[c + 1 for c in row] for row in grid]


def discharge(grid: List[List[int]]) -> List[List[int]]:
    return [[(0 if c > 9 else c) for c in row] for row in grid]


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    octopus_grid: List[List[int]] = read_int_grid(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = count_flashes(grid=octopus_grid, steps=100)
    assert part_1_result == 1721
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = first_synchronized_flash(grid=octopus_grid)
    assert part_2_result == 298
    print('Part 2 result :', part_2_result)
