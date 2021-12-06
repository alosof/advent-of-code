from pathlib import Path
from typing import List

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_int_line


def count_fish_after_n_days(fish_population: List[int], n: int) -> int:
    population_by_timer = {timer: fish_population.count(timer) for timer in range(0, 9)}
    for _ in range(n):
        new_population = {}
        for timer in range(0, 9):
            match timer:
                case 8:
                    new_population[timer] = population_by_timer[0]
                case 6:
                    new_population[timer] = population_by_timer[0] + population_by_timer[7]
                case _:
                    new_population[timer] = population_by_timer[timer + 1]
        population_by_timer = new_population
    return sum(population_by_timer.values())


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    initial_fish_population: List[int] = read_int_line(input_file_path=input_file_path)

    # Part 1
    part_1_result: int = count_fish_after_n_days(fish_population=initial_fish_population, n=80)
    assert part_1_result == 391671
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_fish_after_n_days(fish_population=initial_fish_population, n=256)
    assert part_2_result == 1754000560399
    print('Part 2 result :', part_2_result)
