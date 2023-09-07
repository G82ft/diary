import os
import json

CONFIGS_PATH: str = 'configs/'
DEFAULT_CONFIG: str = 'configs/default.json'
REQUIRED_KEYS: dict = {
    "scale": ("range",),
    "color": ("list",),
    "gradient": ("start", "end"),
    "text": (),
    "checkbox": (),
    "int": (),
    "float": (),
    "bool": (),
    "date": ()
}


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

    return True


def validate_config(path: str) -> None:
    """Raises an appropriate exception, if the config is not valid.

    :raises JSONDecodeError:"""
    if not path.endswith('.json'):
        raise TypeError('The file is not a JSON file!')

    data: dict = {}
    with open(path) as file:
        data |= json.load(file)

    for key in ("columns", "tags"):
        if key not in data:
            raise ValueError(f'Missing a key: {key}!')

    for column in data["columns"]:
        validate_column(column)


def validate_column(column: dict[str]) -> None:
    if "name" not in column:
        raise ValueError('Name of the column is not specified!')

    if "type" not in column:
        raise TypeError('Column type is not specified!')

    if "data" not in column:
        raise ValueError('Column data is missing!')

    if column["type"] not in REQUIRED_KEYS:
        raise TypeError('Unknown column type!')

    for req_key in REQUIRED_KEYS[column["type"]]:
        if req_key not in column["data"]:
            raise ValueError(
                f'Missing required key for type {column["type"]}: "{req_key}"'
            )


def get_default() -> dict:
    if not is_config(DEFAULT_CONFIG):
        raise OSError('Default file is not config!')

    validate_config(DEFAULT_CONFIG)

    with open(DEFAULT_CONFIG) as file:
        data: dict = json.load(file)

    return data
