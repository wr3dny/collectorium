from __future__ import annotations

import json
import os

from schemas.types import Field, FileDef
from utils.parsing import coerce_id


def build_file_path(files_dir: str, file_def: FileDef) -> str:
    return os.path.join(files_dir, file_def.filename)


def load_file(files_dir: str, file_def: FileDef) -> list[Field]:
    path = build_file_path(files_dir, file_def)
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Invalid JSON in: {path}")
        return []
    except OSError as e:
        print(f"Error reading file {path}: {e}")
        return []

    if not isinstance(data, list):
        print(f"Unexpected data format in: {path}")
        return []

    items: list[Field] = []
    for raw in data:
        if isinstance(raw, dict):
            item: Field = dict(raw)
            item[file_def.id_key] = coerce_id(item.get(file_def.id_key))
            items.append(item)

    items.sort(key=lambda r: (r.get(file_def.id_key) is None, r.get(file_def.id_key)))
    return items


def save_file(files_dir: str, file_def: FileDef, records: list[Field]) -> None:
    os.makedirs(files_dir, exist_ok=True)
    path = build_file_path(files_dir, file_def)

    cleaned: list[Field] = []
    for r in records:
        rr: Field = dict(r)
        rr[file_def.id_key] = coerce_id(rr.get(file_def.id_key))
        cleaned.append(rr)

    cleaned.sort(key=lambda r: (r.get(file_def.id_key) is None, r.get(file_def.id_key)))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
