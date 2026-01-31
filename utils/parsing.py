from schemas.types import FileDef, Value


def coerce_id(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s.isdigit():
            return int(s)
    return None


def parse_int_or_none(raw: str) -> int | None:
    s = raw.strip()
    if s == "" or s.lower() == "null":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def parse_bool_or_none(raw: str) -> bool | None:
    s = raw.strip().lower()
    if s == "" or s == "null":
        return None
    if s in {"true", "t", "yes", "y", "1"}:
        return True
    if s in {"false", "f", "no", "n", "0"}:
        return False
    return None


def parse_value_for_key(file_def: FileDef, key: str, raw: str) -> Value:
    """
      - empty input => None (for add)
      - "null" => None
      - int keys -> int|None
      - bool keys -> bool|None
      - otherwise -> string (trimmed) or None
    """

    s = raw.strip()
    if s == "" or s.lower() == "null":
        return None

    if key in file_def.int_keys:
        return parse_int_or_none(s)

    if key in file_def.bool_keys:
        return parse_bool_or_none(s)

    return s


def parse_update_value(file_def: FileDef, key: str, current: Value, raw: str) -> tuple[bool, Value]:
    """
      - Enter/blank => keep current (no update)
      - "null" => set None
      - otherwise parse according to key
    """

    s = raw.strip()
    if s == "":
        return False, current

    if s.lower() == "null":
        return True, None

    new_value = parse_value_for_key(file_def, key, s)

    if key in file_def.bool_keys and new_value is None and s.lower() not in {"null", ""}:
        print("Invalid boolean value. Keeping current.")
        return False, current

    if key in file_def.int_keys and new_value is None and s.lower() not in {"null", ""}:
        print("Invalid integer (or use null). Keeping current.")
        return False, current

    return True, new_value

