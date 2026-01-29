from __future__ import annotations

import json
import os
import sys

from typing import List , Optional

from schemas.types import FILE_DEFS, Field, FileDef

FILES_DIR = "files"


def _coerce_id(value) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s.isdigit():
            return int(s)
    return None


def get_file_def_by_index(index: int) -> Optional[FileDef]:
    if 1 <= index <= len(FILE_DEFS):
        return FILE_DEFS[index - 1]
    return None


def list_files() -> None:
    for i, fd in enumerate(FILE_DEFS, start=1):
        print(f"{i}. {fd.label}")


def build_file_path(file_def: FileDef) -> str:
    return os.path.join(FILES_DIR, file_def.filename)


def load_file(file_def: FileDef) -> List[Field]:
    path = build_file_path(file_def)
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

    items: List[Field] = []
    for raw in data:
        if isinstance(raw, dict):
            item: Field = dict(raw)
            item[file_def.id_key] = _coerce_id(item.get(file_def.id_key))
            items.append(item)

    items.sort(key=lambda b: (b.get(file_def.id_key) is None, b.get(file_def.id_key)))
    return items


def list_records(file_def: FileDef, records: List[Field]) -> None:
    print(f"\nRecords in {file_def.label}:\n")
    for record in records:
        record_id = record.get(file_def.id_key)
        print(f"ID: {record_id}")
        for key, value in record.items():
            if key != file_def.id_key:
                print(f"  {key}: {value}")
        print("----------------")


def add_record(file_def: FileDef, record: Field) -> None:
    pass


def remove_record(file_def: FileDef, record_id: int) -> None:
    pass


def update_record(file_def: FileDef, record: Field) -> None:
    pass


def menu() -> None:
    print("Collectorium\n")
    list_files()
    print("----------------")

    while True:
        print("1. Select file")
        print("2. Exit")
        action = input("Select action: ").strip()

        if action == "1":
            try:
                idx = int(input("Select file: ").strip())
            except ValueError:
                print("Please enter a number.")
                continue

            file_def = get_file_def_by_index(idx)
            if not file_def:
                print("Unknown file selection.")
                continue

            records = load_file(file_def)
            print(f"\nSelected: {file_def.label}")
            print(f"Loaded records: {len(records)}\n")
            list_records(file_def, records)

            # TODO: duplicate from book_store project

        elif action == "2":
            sys.exit(0)
        else:
            print("Invalid action")


if __name__ == "__main__":
    menu()
