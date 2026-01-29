import os
import sys
from numbers import Number
from typing import List


def list_files():
    directory = "files"

    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print(f"The directory '{directory}' does not exist.")
        return

    json_files = [f for f in files if f.lower().endswith(".json")]

    for i, filename in enumerate(json_files, start=1):
        name = os.path.splitext(filename)[0]
        name = name[0].upper() + name[1:] if name else name
        print(f"{i}. {name}")


def file_path(filename: Number) -> str:
    if filename == 1:
        return "books.json"
    elif filename == 2:
        return "lego.json"
    elif filename == 3:
        return "paperModels.json"
    elif filename == 4:
        return "wasgij.json"
    else:
        print("Unknown file")
        return ""

def load_file() -> List[Field]:
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        books: List[Field] = json.load(f)

    for bk in books:
        bk["id"] = _coerce_id(bk.get("id"))

    books.sort(key=lambda b: (b.get("id") is None, b.get("id")))
    return books


def menu():
    print("Collectorium")
    print("")
    list_files()
    print("----------------")
    while True:
        print("1. Select file")
        print("2. Exit")
        action = input("Select action: ")
        if action == "1":
            while True:
                file = int(input("Select file: "))
                file_path(file)
        elif action == "2":
            sys.exit(0)
        else:
            print("Invalid action")


if __name__ == "__main__":
    menu()
