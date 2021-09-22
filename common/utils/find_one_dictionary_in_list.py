from typing import List, Dict, Union, Any


def find_one_dictionary_in_list(array: List[Dict], key: str, value: Any) -> Union[Dict, None]:
    for index, item in enumerate(array):
        if item.get(key) == value:
            return index, item
    return None
