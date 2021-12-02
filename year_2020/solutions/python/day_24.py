import os
from typing import List, Tuple, Dict

from year_2020.solutions.python.utils.files import INPUTS_FOLDER, read_lines
from year_2020.solutions.python.utils.timing import timer


@timer
def count_black_tiles_after_animations(tiles_to_flip: List[str], days: int) -> int:
    floor: Dict[Tuple[int, int], int] = install_tile_floor(tiles_to_flip)
    for _ in range(days):
        floor = animate_tiles(floor)
    return sum(floor.values())


def animate_tiles(floor: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
    floor_with_borders: Dict[Tuple[int, int], int] = add_border_around_external_black_tiles(floor)
    new_floor: Dict[Tuple[int, int], int] = {}
    for tile in floor_with_borders:
        tile_color: int = floor_with_borders[tile]
        black_adjacent_tiles: int = count_black_adjacent_tiles(tile, floor_with_borders)
        if tile_color == 1 and (black_adjacent_tiles == 0 or black_adjacent_tiles > 2):
            new_floor[tile] = 0
        elif tile_color == 0 and black_adjacent_tiles == 2:
            new_floor[tile] = 1
        else:
            new_floor[tile] = tile_color
    return new_floor


def add_border_around_external_black_tiles(floor: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
    floor_with_border: Dict[Tuple[int, int], int] = {}
    for tile in floor:
        floor_with_border[tile] = floor[tile]
        if floor[tile] == 1:
            adj_tiles: List[Tuple[int, int]] = adjacent_tiles(tile)
            for t in adj_tiles:
                if t not in floor_with_border:
                    floor_with_border[t] = 0
    return floor_with_border


def count_black_adjacent_tiles(tile: Tuple[int, int], floor: Dict[Tuple[int, int], int]) -> int:
    return sum([floor[t] for t in adjacent_tiles(tile) if t in floor])


def adjacent_tiles(tile_coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    offsets: List[Tuple[int, int]] = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]
    return [(tile_coords[0] + offset_x, tile_coords[1] + offset_y) for offset_x, offset_y in offsets]


@timer
def count_black_tiles_after_floor_is_installed(tiles_to_flip: List[str]) -> int:
    floor: Dict[Tuple[int, int], int] = install_tile_floor(tiles_to_flip)
    return sum(floor.values())


def install_tile_floor(tiles_to_flip: List[str]) -> Dict[Tuple[int, int], int]:
    floor: Dict[Tuple[int, int], int] = {}
    for tile_path in tiles_to_flip:
        tile_coordinates: Tuple[int, int] = coordinates(tile_path)
        floor[tile_coordinates] = 1 - floor.get(tile_coordinates, 0)
    return floor


def coordinates(tile_path: str) -> Tuple[int, int]:
    i = 0
    x = 0
    y = 0
    while i < len(tile_path):
        instruction = tile_path[i]
        if instruction == 'e':
            x += 1
            i += 1
        elif instruction == 'w':
            x -= 1
            i += 1
        elif instruction == 's':
            y -= 1
            i += 1
            instruction = tile_path[i]
            if instruction == 'e':
                i += 1
            elif instruction == 'w':
                x -= 1
                i += 1
        elif instruction == 'n':
            y += 1
            i += 1
            instruction = tile_path[i]
            if instruction == 'e':
                x += 1
                i += 1
            elif instruction == 'w':
                i += 1
    return x, y


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_24', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = count_black_tiles_after_floor_is_installed(tiles_to_flip=input_list)
    assert part_1_result == 282
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_black_tiles_after_animations(tiles_to_flip=input_list, days=100)
    assert part_2_result == 3445
    print('Part 2 result :', part_2_result)
