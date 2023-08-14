import os
import json

CONFIGS_PATH: str = 'configs/'
DEFAULT_CONFIG: str = 'configs/default.json'


def get_configs():
    names: list[str] = os.listdir(CONFIGS_PATH)
    total: int = len(names)

    yield 0, total, ''

    for i, name in enumerate(names):
        path: str = CONFIGS_PATH + name
        if not os.path.isfile(path):
            yield i, total, ''
            continue

        if not is_config(path):
            yield i, total, ''
            continue

        yield i, total, name


def is_config(path: str) -> bool:
    if not path.endswith('.json'):
        return False

    data: dict = {}
    with open(path) as file:
        try:
            data |= json.load(file)
        except json.JSONDecodeError:
            return False

    if any(key not in data for key in ("columns", "tags")):
        return False

    return True


def get_default() -> dict:
    if not is_config(DEFAULT_CONFIG):
        raise OSError('Default file is not config!')

    with open(DEFAULT_CONFIG) as file:
        data: dict = json.load(file)

    return data
