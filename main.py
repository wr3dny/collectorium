from __future__ import annotations

import json
import os
import sys

from typing import Optional

from schemas.types import FILE_DEFS, Field, FileDef
from storage.json_storage import load_file, save_file

from utils.parsing import (
    coerce_id,
    parse_int_or_none,
    parse_bool_or_none,
    parse_value_for_key,
    parse_update_value,
)

FILES_DIR = "files"


def get_file_def_by_index(index: int) -> Optional[FileDef]:
    if 1 <= index <= len(FILE_DEFS):
        return FILE_DEFS[index - 1]
    return None


def list_files() -> None:
    print("\nAvailable Files:")
    print("------------------")
    for i, fd in enumerate(FILE_DEFS, start=1):
        print(f"{i}. {fd.label}")



def _fmt(value) -> str:
    return "" if value is None else str(value)


def list_records(file_def: FileDef, records: list[Field]) -> None:
    print(f"\nRecords in {file_def.label}:\n")
    if not records:
        print("(no records)")
        return

    for record in records:
        record_id = record.get(file_def.id_key)
        print(f"ID: {record_id}")

        for key, label in file_def.fields:
            print(f"  {label}: {_fmt(record.get(key))}")

        print("----------------")


def next_id(file_def: FileDef, records: list[Field]) -> Optional[int]:
    existing_ids: set[int] = set()

    for r in records:
        v = r.get(file_def.id_key)
        if isinstance(v, int):
            existing_ids.add(v)

    for i in range(1, max(existing_ids, default=0) + 2):
        if i not in existing_ids:
            return i

    return None



def _find_record_index_by_id(file_def: FileDef, records: list[Field], record_id: int) -> int | None:
    for idx, r in enumerate(records):
        if r.get(file_def.id_key) == record_id:
            return idx
    return None


def add_record(file_def: FileDef) -> Field:
    records = load_file(FILES_DIR, file_def)
    new_id = next_id(file_def, records)

    new_record: Field = {file_def.id_key: new_id}

    print(f"Adding new book with ID: {new_id}")
    print('Press Space or Enter to skip category, type "null" to leave field empty')

    for key, label in file_def.fields:
        raw = input(f"{label}: ")
        new_record[key] = parse_value_for_key(file_def, key, raw)

    records.append(new_record)
    save_file(FILES_DIR, file_def, records)

    print("Record added.\n")
    return new_record


def update_record(file_def: FileDef, record_id: int | None) -> Field | None:
    if record_id is None:
        print("No ID selected.")
        return None

    records = load_file(FILES_DIR, file_def)
    idx = _find_record_index_by_id(file_def, records, record_id)
    if idx is None:
        print("No record found with this ID.")
        return None

    existing = dict(records[idx])

    print(f"\nUpdating {file_def.label}: {record_id}")
    print("Press Enter to keep current value. \nType 'null' to clear.")

    for key, label in file_def.fields:
        current_value = existing.get(key)
        print(f'{key}: {current_value}')
        print(f"{label} (current: {current_value})")
        raw = input("New value: ")
        should_update, new_value = parse_update_value(file_def, key, current_value, raw)
        if should_update:
            existing[key] = new_value

    records[idx] = existing
    save_file(FILES_DIR, file_def, records)

    print("Record updated.\n")
    return existing


def delete_record(file_def: FileDef, record_id: int | None) -> bool:
    if record_id is None:
        print("No ID selected.")
        return False

    records = load_file(FILES_DIR, file_def)
    before = len(records)

    records = [r for r in records if r.get(file_def.id_key) != record_id]

    if len(records) == before:
        print("No record found with this ID.")
        return False

    save_file(FILES_DIR, file_def, records)
    print("Record deleted.\n")
    return True

def _file_menu(file_def: FileDef) -> None:
        while True:
            records = load_file(FILES_DIR, file_def)

            print(f"\nSelected: {file_def.label} (records: {len(records)})")
            print("1. List records")
            print("2. Add record")
            print("3. Update record")
            print("4. Delete record")
            print("5. Back")
            print("6. Exit")

            action = input("Select action: ").strip()

            if action == "1":
                list_records(file_def, records)

            elif action == "2":
                add_record(file_def)

            elif action == "3":
                try:
                    rid = int(input("Enter ID to update: ").strip())
                except ValueError:
                    print("Please enter a number.")
                    continue
                update_record(file_def, rid)

            elif action == "4":
                try:
                    rid = int(input("Enter ID to delete: ").strip())
                except ValueError:
                    print("Please enter a number.")
                    continue
                delete_record(file_def, rid)

            elif action == "5":
                return

            elif action == "6":
                sys.exit(0)

            else:
                print("Invalid action.")

def menu() -> None:
    print("Collectorium\n")

    while True:
        print("----------------")
        print("1. Select file")
        print("2. Exit")
        action = input("Select action: ").strip()

        if action == "1":
            list_files()
            try:
                idx = int(input("Select file:").strip())
            except ValueError:
                print("Please enter a number.")
                continue

            file_def = get_file_def_by_index(idx)
            if not file_def:
                print("Unknown file selection.")
                continue

            _file_menu(file_def)

        elif action == "2":
            sys.exit(0)
        else:
            print("Invalid action")


if __name__ == "__main__":
    menu()
