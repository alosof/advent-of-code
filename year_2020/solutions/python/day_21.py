import os
from functools import reduce
from itertools import product
from operator import itemgetter
from typing import Dict, List, Set, Tuple

from year_2020.solutions.python.utils.dict import remove_key_from_mapping, remove_value_from_mapping
from year_2020.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def get_ordered_list_of_allergenic_ingredients(descriptions: List[str]) -> str:
    potential_ingredients_by_allergen, _ = parse_foods_descriptions(descriptions)
    allergen_mapping: Dict[str, str] = assign_allergens_to_ingredients(potential_ingredients_by_allergen, {})
    return ','.join(map(lambda x: x[1], sorted(allergen_mapping.items(), key=itemgetter(0))))


def assign_allergens_to_ingredients(potential_ingredients_by_allergen: Dict[str, Set[str]],
                                    allergen_mapping: Dict[str, str]) -> Dict[str, str]:
    if len(potential_ingredients_by_allergen) == 0:
        return allergen_mapping
    else:
        ingredient_with_least_possibilities = find_ingredient_with_min_allergens(potential_ingredients_by_allergen)
        allergen = list(potential_ingredients_by_allergen[ingredient_with_least_possibilities])[0]
        allergen_mapping[ingredient_with_least_possibilities] = allergen
        potential_ingredients_by_allergen = remove_key_from_mapping(ingredient_with_least_possibilities,
                                                                    potential_ingredients_by_allergen)
        potential_ingredients_by_allergen = remove_value_from_mapping(allergen, potential_ingredients_by_allergen)
        return assign_allergens_to_ingredients(potential_ingredients_by_allergen, allergen_mapping)


def find_ingredient_with_min_allergens(potential_ingredients_by_allergen: Dict[str, Set[str]]) -> str:
    return min(potential_ingredients_by_allergen, key=lambda x: len(potential_ingredients_by_allergen[x]))


def count_non_allergenic_ingredients_occurrences(descriptions: List[str]) -> int:
    potential_ingredients_by_allergen, all_foods = parse_foods_descriptions(descriptions)
    all_ingredients: Set[str] = reduce(lambda x, y: x.union(y), all_foods)
    allergenic_ingredients: Set[str] = reduce(lambda x, y: x.union(y), potential_ingredients_by_allergen.values())
    non_allergenic_ingredients: Set[str] = all_ingredients.difference(allergenic_ingredients)
    return sum(ingredient in food for ingredient, food in product(non_allergenic_ingredients, all_foods))


def parse_foods_descriptions(foods_descriptions: List[str]) -> Tuple[Dict[str, Set[str]], List[Set[str]]]:
    all_foods: List[Set[str]] = []
    potential_ingredients: Dict[str, Set[str]] = {}
    for description in foods_descriptions:
        raw_ingredients, raw_allergens = description.split(' (contains ')
        ingredients: Set[str] = set(raw_ingredients.split(' '))
        all_foods.append(ingredients)
        allergens = raw_allergens.strip(')').split(', ')
        for allergen in allergens:
            if allergen not in potential_ingredients:
                potential_ingredients[allergen] = set(ingredients)
            else:
                potential_ingredients[allergen] = potential_ingredients[allergen].intersection(ingredients)
    return potential_ingredients, all_foods


if __name__ == "__main__":
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_21', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = count_non_allergenic_ingredients_occurrences(descriptions=input_list)
    assert part_1_result == 1945
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: str = get_ordered_list_of_allergenic_ingredients(descriptions=input_list)
    assert part_2_result == 'pgnpx,srmsh,ksdgk,dskjpq,nvbrx,khqsk,zbkbgp,xzb'
    print('Part 2 result :', part_2_result)
