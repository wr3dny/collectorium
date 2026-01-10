import os
import sys


def file_path(filename: str) -> str:
    if filename == "books.json":
        return "books.json"
    elif filename == "lego.json":
        return "lego.json"
    elif filename == "paperModels.json":
        return "paperModels.json"
    else:
        print("Unknown file")
        return ""


def list_files():
    directory = "files"

    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print(f"The directory '{directory}' does not exist.")
        return

    for filename in files:
        if filename.lower().endswith('.json'):
            name = os.path.splitext(filename)[0]
            name = name[0].upper() + name[1:]
            print(name)


def menu():
    print("Collectorium")
    print("")
    list_files()
    print("----------------")

    while True:
        print("1. Chose file")
        print("2. List file")
        print("5. Exit")

        action = input("Enter number : ")

        if action == "1":
            while True:
                print("1. Books")
                print("2. Lego")
                print("3. Paper Models")
                print("4. Return main menu")
                sub = input("Enter number : ").strip()
                if sub == "1":
                    file = "books.json"
                    return file_path(file)
                elif sub == "2":
                    file = "lego.json"
                    return file_path(file)
                elif sub == "3":
                    file = "paperModels.json"
                    return file_path(file)
                elif sub == "4":
                    break
                else:
                    print("Invalid choice.")

        elif action == "5":
            sys.exit(0)
        else:
            print("Invalid action")


if __name__ == "__main__":
    menu()
