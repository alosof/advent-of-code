import os
import re
from copy import deepcopy
from math import prod, sqrt
from typing import List, Dict, Set

from year_2020.solutions.python.utils.files import INPUTS_FOLDER


def evaluate_water_roughness(tiles: Dict[int, List[List[str]]]) -> int:
    possible_border_hashes_by_tile: Dict[int, Set[int]] = all_possible_border_hashes_by_tile(tiles)
    possible_neighbors: Dict[int, Set[int]] = neighbors_by_tile(possible_border_hashes_by_tile)
    blueprint: List[List[int]] = tile_positions_blueprint(possible_neighbors)
    ajusted_tiles_grid: List[List[List[List[str]]]] = adjust_tiles_grid(tiles, blueprint)
    tiles_grid_without_borders: List[List[List[List[str]]]] = remove_borders(ajusted_tiles_grid)
    image: List[List[str]] = assemble_image(tiles_grid_without_borders)
    monster_pattern: List[List[str]] = \
        [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' '],
         ['#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#'],
         [' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ']]
    monsters_count: int = count_monsters(image, monster_pattern)
    return count_hashtags(image) - monsters_count * count_hashtags(monster_pattern)


def count_hashtags(patch: List[List[str]]) -> int:
    return sum(c == '#' for r in patch for c in r)


def count_monsters(image: List[List[str]], monster_pattern: List[List[str]]) -> int:
    monsters_count = 0
    for transformed_image in transformations(image):
        for i in range(len(transformed_image)):
            for j in range(len(transformed_image[0])):
                patch = [r[j:j + len(monster_pattern[0])] for r in transformed_image[i:i + len(monster_pattern)]]
                if size(patch) == size(monster_pattern) and is_monster(patch, monster_pattern):
                    monsters_count += 1
        if monsters_count > 0:
            break
    return monsters_count


def is_monster(patch: List[List[str]], monster_pattern: List[List[str]]) -> bool:
    found = True
    for r in range(len(patch)):
        for c in range(len(patch[0])):
            found = found and (True if monster_pattern[r][c] == ' ' else patch[r][c] == monster_pattern[r][c])
    return found


def size(patch: List[List[str]]) -> int:
    return len(patch[0]) * len(patch)


def assemble_image(tiles_grid_without_borders: List[List[List[List[str]]]]) -> List[List[str]]:
    image = []
    for tiles_row in tiles_grid_without_borders:
        image.extend(assemble_tiles_row(tiles_row))
    return image


def assemble_tiles_row(tiles_row: List[List[List[str]]]) -> List[List[str]]:
    new_rows = [[] for _ in range(len(tiles_row[0]))]
    for tile in tiles_row:
        for i in range(len(tile)):
            new_rows[i].extend(tile[i])
    return new_rows


def remove_borders(tiles_grid: List[List[List[List[str]]]]) -> List[List[List[List[str]]]]:
    rows, cols = len(tiles_grid), len(tiles_grid[0])
    tiles_grid_without_borders: List[list] = [[None for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            tile_with_borders = tiles_grid[row][col]
            tiles_grid_without_borders[row][col] = [r[1:-1] for r in tile_with_borders[1:-1]]
    return tiles_grid_without_borders


def adjust_tiles_grid(tiles: Dict[int, List[List[str]]], blueprint: List[List[int]]) -> List[List[List[List[str]]]]:
    rows, cols = len(blueprint), len(blueprint[0])
    tiles_grid: List[list] = [[None for _ in range(cols)] for _ in range(rows)]
    for t_a in transformations(tiles[blueprint[0][0]]):
        for t_b in transformations(tiles[blueprint[1][0]]):
            for t_c in transformations(tiles[blueprint[0][1]]):
                if is_correct_match(t_a, t_b, 'down') and is_correct_match(t_a, t_c, 'right'):
                    tiles_grid[0][0] = t_a
                    tiles_grid[1][0] = t_b
                    tiles_grid[0][1] = t_c
    for i in range(2, len(tiles_grid)):
        for t in transformations(tiles[blueprint[i][0]]):
            if is_correct_match(tiles_grid[i - 1][0], t, 'down'):
                tiles_grid[i][0] = t
    for j in range(2, len(tiles_grid[0])):
        for t in transformations(tiles[blueprint[0][j]]):
            if is_correct_match(tiles_grid[0][j - 1], t, 'right'):
                tiles_grid[0][j] = t
    for i in range(1, len(tiles_grid)):
        for j in range(1, len(tiles_grid[0])):
            for t in transformations(tiles[blueprint[i][j]]):
                if is_correct_match(tiles_grid[i - 1][j], t, 'down') and is_correct_match(tiles_grid[i][j - 1], t,
                                                                                          'right'):
                    tiles_grid[i][j] = t
    return tiles_grid


def is_correct_match(first_tile: List[List[str]], second_tile: List[List[str]], relative_position: str) -> bool:
    if relative_position == 'right':
        return all(a == b for a, b in zip([r[-1] for r in first_tile], [r[0] for r in second_tile]))
    if relative_position == 'down':
        return all(a == b for a, b in zip(first_tile[-1], second_tile[0]))


def transformations(tile: List[List[str]]) -> List[List[List[str]]]:
    return [tile,
            rotate(tile),
            rotate(rotate(tile)),
            rotate(rotate(rotate(tile))),
            flip(tile),
            rotate(flip(tile)),
            rotate(rotate(flip(tile))),
            rotate(rotate(rotate(flip(tile))))]


def flip(tile: List[List[str]]) -> List[List[str]]:
    return list(reversed(tile))


def rotate(tile: List[List[str]]) -> List[List[str]]:
    new_tile = deepcopy(tile)
    rows = len(new_tile)
    cols = len(new_tile[0])
    for i in range(rows):
        for j in range(cols):
            new_tile[i][j] = tile[cols - 1 - j][i]
    return new_tile


def tile_positions_blueprint(neighbors: Dict[int, Set[int]]) -> List[List[int]]:
    blueprint_size: int = int(sqrt(len(neighbors)))
    blueprint: List[List[int]] = [[0 for _ in range(blueprint_size)] for _ in range(blueprint_size)]
    corner_tiles_ids: List[int] = [n for n in neighbors if len(neighbors[n]) < 3]
    starting_tile_id: int = corner_tiles_ids[-1]
    blueprint[0][0] = starting_tile_id
    for diag_sum in range(1, 2 * blueprint_size - 1):
        to_fill = [(k, diag_sum - k) for k in range(1, diag_sum) if
                   k < blueprint_size and diag_sum - k < blueprint_size]
        for i, j in to_fill:
            upper_tile_neighbors: Set[int] = neighbors[blueprint[i - 1][j]]
            left_tile_neighbors: Set[int] = neighbors[blueprint[i][j - 1]]
            common_neighbors_of_up_and_left = upper_tile_neighbors.intersection(left_tile_neighbors)
            upper_left_tile_id: int = blueprint[i - 1][j - 1]
            candidates = common_neighbors_of_up_and_left.difference([upper_left_tile_id])
            blueprint[i][j] = list(candidates)[0]
        if diag_sum < blueprint_size:
            blueprint[0][diag_sum] = list(neighbors[blueprint[0][diag_sum - 1]]
                                          .difference([blueprint[0][diag_sum - 2], blueprint[1][diag_sum - 1]]))[0]
            blueprint[diag_sum][0] = list(neighbors[blueprint[diag_sum - 1][0]]
                                          .difference([blueprint[diag_sum - 2][0], blueprint[diag_sum - 1][1]]))[0]
    return blueprint


def multiply_corner_tiles_ids(tiles: Dict[int, List[List[str]]]) -> int:
    possible_border_hashes_by_tile: Dict[int, Set[int]] = all_possible_border_hashes_by_tile(tiles)
    possible_neighbors: Dict[int, Set[int]] = neighbors_by_tile(possible_border_hashes_by_tile)
    corner_tile_ids: List[int] = [n for n in possible_neighbors if len(possible_neighbors[n]) < 3]
    return prod(corner_tile_ids)


def neighbors_by_tile(border_hashes: Dict[int, Set[int]]) -> Dict[int, Set[int]]:
    neighbors = {}
    for tile_i in border_hashes:
        neighbors[tile_i] = set()
        for tile_j in border_hashes:
            if tile_j != tile_i and len(border_hashes[tile_i].intersection(border_hashes[tile_j])) > 0:
                neighbors[tile_i].add(tile_j)
    return neighbors


def all_possible_border_hashes_by_tile(tiles: Dict[int, List[List[str]]]) -> Dict[int, Set[int]]:
    return {tile_id: set([binary_hash(border) for border in all_possible_borders(tiles[tile_id])]) for tile_id in tiles}


def all_possible_borders(tile: List[List[str]]) -> List[List[str]]:
    upper = tile[0]
    right = [r[-1] for r in tile]
    lower = list(reversed(tile[-1]))
    left = list(reversed([r[0] for r in tile]))
    flipped_upper = list(reversed(upper))
    flipped_right = list(reversed(right))
    flipped_lower = list(reversed(lower))
    flipped_left = list(reversed(left))
    return [upper, right, lower, left, flipped_upper, flipped_right, flipped_lower, flipped_left]


def binary_hash(border: List[str]) -> int:
    return int(''.join(border).replace('#', '1').replace('.', '0'), base=2)


def read_tiles(input_path: str) -> Dict[int, List[List[str]]]:
    tiles: Dict[int, List[List[str]]] = {}
    with open(input_path, 'r') as input_file:
        blocks = [block.split('\n') for block in input_file.read().strip().split('\n\n')]
        for block in blocks:
            tile_id: int = int(re.search(r'\d{4}', block[0]).group())
            tile: List[List[str]] = [list(line) for line in block[1:]]
            tiles[tile_id] = tile
    return tiles


if __name__ == "__main__":
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_20', 'input.txt')
    tiles_dict: Dict[int, List[List[str]]] = read_tiles(input_path=input_file_path)

    # Part 1
    part_1_result: int = multiply_corner_tiles_ids(tiles=tiles_dict)
    assert part_1_result == 66020135789767
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = evaluate_water_roughness(tiles=tiles_dict)
    assert part_2_result == 1537
    print('Part 2 result :', part_2_result)
