from __future__ import annotations

import json
import os
import sys

from typing import Optional

from schemas.types import FILE_DEFS, Field, FileDef

FILES_DIR = "files"


def _coerce_id(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s.isdigit():
            return int(s)
    return None


def _parse_int_or_none(raw: str) -> int | None:
    s = raw.strip()
    if s == "" or s.lower() == "null":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _parse_bool_or_none(raw: str) -> bool | None:
    s = raw.strip().lower()
    if s == "" or s == "null":
        return None
    if s in {"true", "t", "yes", "y", "1"}:
        return True
    if s in {"false", "f", "no", "n", "0"}:
        return False
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


def load_file(file_def: FileDef) -> list[Field]:
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

    items: list[Field] = []
    for raw in data:
        if isinstance(raw, dict):
            item: Field = dict(raw)
            item[file_def.id_key] = _coerce_id(item.get(file_def.id_key))
            items.append(item)

    items.sort(key=lambda b: (b.get(file_def.id_key) is None, b.get(file_def.id_key)))
    return items


def list_records(file_def: FileDef, records: list[Field]) -> None:
    print(f"\nRecords in {file_def.label}:\n")
    for record in records:
        record_id = record.get(file_def.id_key)
        print(f"ID: {record_id}")
        for key, value in record.items():
            if key != file_def.id_key:
                print(f"  {key}: {value}")
        print("----------------")


# def next_id(file_def: FileDef list[Field]) -> Optional[int]:
#     existing_ids = set()
#     for f in field:
#         v = b.get("id")
#         if isinstance(v, int):
#             existing_ids.add(v)
#
#     for i in range(1, max(existing_ids, default=0) + 2):
#         if i not in existing_ids:
#             return i
#     return None


def add_record(file_def: FileDef, record: Field) -> None:
    pass


def update_record(file_def: FileDef, record: Field) -> None:
    pass

def delete_record(file_def: FileDef, record_id: int) -> None:
    pass

def save_record(file_def: FileDef, record: Field) -> None:


"""
reuse
"""

def save_books(books: list[Book]) -> None:
    books_sorted = sorted(books, key=lambda b: (b.get("id") is None, b.get("id")))
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(books_sorted, f, indent=4, ensure_ascii=False)


def next_id(books: list[Book]) -> Optional[int]:
    existing_ids = set()
    for b in books:
        v = b.get("id")
        if isinstance(v, int):
            existing_ids.add(v)

    for i in range(1, max(existing_ids, default=0) + 2):
        if i not in existing_ids:
            return i
    return None


def remove_book(book_id: int) -> bool:
    books = load_books()
    filtered = [b for b in books if b["id"] != book_id]

    if len(books) == len(filtered):
        return False

    save_books(filtered)
    return True



def _parse_int_or_none(raw: str) -> Optional[int]:
    s = raw.strip()
    if s == "":
        return None
    if s.lower() == "null":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def add_book() -> Book:
    books = load_books()
    new_book_id = next_id(books)

    book: Book = {"id": new_book_id}

    print(f"Adding new book with ID: {new_book_id}")
    print('Press Space or Enter to skip category, type "null" to leave field empty')

    for key, label in BOOK_FIELDS:
        raw = input(f"{label}: ").strip()

        if raw.lower() == "null" or raw == "":
            value: BookValue = None
        else:
            if key in {"numberInSeries", "numberInSubSeries"}:
                parsed = _parse_int_or_none(raw)
                value = parsed
            else:
                value = raw

        book[key] = value

    books.append(book)
    save_books(books)
    print("Book added.")
    return book


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
