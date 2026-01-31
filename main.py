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
    for i, fd in enumerate(FILE_DEFS, start=1):
        print(f"{i}. {fd.label}")



def list_records(file_def: FileDef, records: list[Field]) -> None:
    print(f"\nRecords in {file_def.label}:\n")
    for record in records:
        record_id = record.get(file_def.id_key)
        print(f"ID: {record_id}")
        for key, value in record.items():
            if key != file_def.id_key:
                print(f"  {key}: {value}")
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


def update_record(file_def: FileDef, record: Field) -> None:
    pass

def delete_record(file_def: FileDef, record_id: int) -> None:
    pass

"""
reuse
"""




def remove_book(book_id: int) -> bool:
    books = load_books()
    filtered = [b for b in books if b["id"] != book_id]

    if len(books) == len(filtered):
        return False

    save_books(filtered)
    return True




def update_book(book_id: int | None) -> Book | None:
    if book_id is None:
        print("No ID selected. Choose another ID or exit to menu.")
        return None

    books = load_books()

    for idx, existing in enumerate(books):
        if existing.get("id") == book_id:
            print(f'Chosen ID: {existing["id"]} - {existing["author"]} - {existing["title"]}')
            print('Press Space or Enter to skip category, type "null" to clear field')

            for key in list(existing.keys()):
                if key == "id":
                    continue

                current_value = existing.get(key)
                print(f'{key}: {current_value}')

                raw = input("New value: ")
                should_update, new_value = _parse_new_value(current_value, raw)

                if should_update:
                    existing[key] = new_value

            books[idx] = existing
            save_books(books)

            print("Book updated.")
            return existing

    print("No book found with this ID. Choose another ID or exit to menu.")
    return None

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
