from pathlib import Path
from typing import Dict, List

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def paths_with_one_small_cave_visited_at_most_twice(cave_system: Dict[str, List[str]], current_cave: str,
                                                    path: List[str]) -> int:
    if (current_cave not in cave_system) or (cave_system[current_cave] == []):
        return 0
    elif current_cave == 'end':
        return 1
    else:
        path = path + [current_cave]
        updated_cave_system = cave_system
        if is_endpoint(current_cave) or is_small(current_cave) and at_least_one_small_cave_visited_twice(path):
            updated_cave_system = remove_cave(current_cave, updated_cave_system)
        if at_least_one_small_cave_visited_twice(path):
            visited_small_caves = count_small_caves_visits(path).keys()
            visited_small_caves_still_in_cave_system = set(visited_small_caves).intersection(updated_cave_system.keys())
            for cave in visited_small_caves_still_in_cave_system:
                updated_cave_system = remove_cave(cave, updated_cave_system)
        return sum([paths_with_one_small_cave_visited_at_most_twice(updated_cave_system, next_cave, path)
                    for next_cave in cave_system[current_cave]])


def paths_with_small_caves_visited_at_most_once(cave_system: Dict[str, List[str]], current_cave: str) -> int:
    if current_cave == 'end':
        return 1
    else:
        if is_endpoint(current_cave) or is_small(current_cave):
            updated_cave_system = remove_cave(current_cave, cave_system)
        else:
            updated_cave_system = cave_system
        return sum([paths_with_small_caves_visited_at_most_once(updated_cave_system, next_cave)
                    for next_cave in cave_system[current_cave]])


def at_least_one_small_cave_visited_twice(path: List[str]) -> bool:
    return any(cave_visits > 1 for cave_visits in count_small_caves_visits(path).values())


def count_small_caves_visits(path: List[str]) -> Dict[str, int]:
    return {cave: path.count(cave) for cave in path if is_small(cave)}


def remove_cave(cave: str, cave_system: Dict[str, List[str]]) -> Dict[str, List[str]]:
    return {k: [e for e in v if e != cave] for k, v in cave_system.items() if k != cave}


def is_small(cave: str) -> bool:
    return not is_endpoint(cave) and (cave.lower() == cave)


def is_endpoint(cave: str) -> bool:
    return cave in ['start', 'end']


def build_cave_system(input_lines: List[str]) -> Dict[str, List[str]]:
    cave_system = {}
    for path in input_lines:
        cave_1, cave_2 = path.split('-')
        cave_system[cave_1] = cave_system.get(cave_1, []) + [cave_2]
        cave_system[cave_2] = cave_system.get(cave_2, []) + [cave_1]
    return cave_system


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    cave_map: Dict[str, List[str]] = build_cave_system(read_lines(input_file_path=input_file_path, line_type=str))

    # Part 1
    part_1_result: int = paths_with_small_caves_visited_at_most_once(cave_system=cave_map, current_cave='start')
    assert part_1_result == 3450
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = paths_with_one_small_cave_visited_at_most_twice(cave_system=cave_map,
                                                                         current_cave='start',
                                                                         path=[])
    assert part_2_result == 96528
    print('Part 2 result :', part_2_result)
