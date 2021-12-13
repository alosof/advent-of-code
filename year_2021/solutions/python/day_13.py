from pathlib import Path
from typing import List, Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def number_of_dots_after_one_fold(dots: List[Tuple[int, int]], folds: List[Tuple[str, int]]) -> int:
    dots_after_one_fold, _ = fold(dots, [folds[0]])
    return len(dots_after_one_fold)


def fold(dots: List[Tuple[int, int]], folds: List[Tuple[str, int]]) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    new_dots = dots
    new_shape = get_shape(dots)
    for _fold in folds:
        axis, position = _fold
        if axis == 'x':
            new_dots = vertical_fold(new_dots, position)
            new_shape = (new_shape[0], position)
        elif axis == 'y':
            new_dots = horizontal_fold(new_dots, position)
            new_shape = (position, new_shape[1])
    return new_dots, new_shape


def vertical_fold(dots: List[Tuple[int, int]], x: int) -> List[Tuple[int, int]]:
    new_dots = []
    for dot in dots:
        if dot[0] < x:
            new_dots.append(dot)
        elif dot[0] > x:
            new_dots.append((2 * x - dot[0], dot[1]))
    return list(set(new_dots))


def horizontal_fold(dots: List[Tuple[int, int]], y: int) -> List[Tuple[int, int]]:
    new_dots = []
    for dot in dots:
        if dot[1] < y:
            new_dots.append(dot)
        elif dot[1] > y:
            new_dots.append((dot[0], 2 * y - dot[1]))
    return list(set(new_dots))


def get_shape(dots: List[Tuple[int, int]]) -> Tuple[int, int]:
    return max([d[0] for d in dots]) + 1, max([d[1] for d in dots]) + 1


def to_grid(dots: List[Tuple[int, int]], shape: Tuple[int, int]) -> List[List[str]]:
    grid = [['.' for _ in range(shape[1])] for _ in range(shape[0])]
    for dot in dots:
        grid[dot[1]][dot[0]] = "#"
    return grid


def render(grid: List[List[str]]) -> str:
    return "\n".join([' '.join(row) for row in grid])


def read_folding_instructions(input_path: Path) -> Tuple[List[Tuple[int, int]], List[Tuple[str, int]]]:
    lines = read_lines(input_path, str)
    separator = lines.index('')
    dots = []
    folds = []
    for line in lines[:separator]:
        dot = line.split(',')
        dots.append((int(dot[0]), int(dot[1])))
    for line in lines[(separator + 1):]:
        axis, position = line.split('fold along ')[-1].split("=")
        folds.append((axis, int(position)))
    return dots, folds


def read_saved_result(result_path: Path) -> str:
    with open(result_path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    result_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'result.txt'
    input_dots, input_folds = read_folding_instructions(input_file_path)

    # Part 1
    part_1_result: int = number_of_dots_after_one_fold(input_dots, input_folds)
    assert part_1_result == 770
    print('Part 1 result :', part_1_result)

    # Part 2
    dots_after_folding, shape_after_folding = fold(input_dots, input_folds)
    rendered_grid_after_folding = render(to_grid(dots_after_folding, shape_after_folding))
    rendered_expected_grid = read_saved_result(result_file_path)
    assert rendered_expected_grid == rendered_grid_after_folding
    print('Part 2 result :')
    print(rendered_grid_after_folding)
