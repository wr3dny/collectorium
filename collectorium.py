import sys


def menu():
    while True:
        print("Book Store Menu")
        print("1. List all books")
        print("2. Add book")
        print("3. Update book")
        print("4. Remove book")
        print("5. Exit")

        choice = input("Enter number : ")

        if choice == "1":
            pass

        elif choice == "2":
            pass

        # elif choice == "3":
        #     while True:
        #         print("1. Choose id")
        #         print("2. Return main menu")
        #         sub = input("Enter number : ").strip()
        #         if sub == "1":
        #             try:
        #                 book_id = int(input("Enter book ID: ").strip())
        #             except ValueError:
        #                 print("Invalid ID.")
        #                 continue
        #             update_book(book_id)
        #         elif sub == "2":
        #             break
        #         else:
        #             print("Invalid choice.")
        # elif choice == "4":
        #     try:
        #         book_id = int(input("Enter book ID to remove: ").strip())
        #     except ValueError:
        #         print("Invalid ID.")
        #         continue
        #
        #     if remove_book(book_id):
        #         print("Book removed.")
        #     else:
        #         print("No book found with this ID.")

        elif choice == "5":
            sys.exit(0)
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()
