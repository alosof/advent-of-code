def remove_key_from_mapping(key_to_remove, mapping: dict) -> dict:
    return {key: mapping[key] for key in mapping if key != key_to_remove}


def remove_value_from_mapping(value_to_remove, mapping: dict) -> dict:
    for pos in mapping:
        mapping[pos] = mapping[pos].difference([value_to_remove])
    return mapping
