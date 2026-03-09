from datetime import date
from src.models import Library, SimpleFinePolicy

def main():
    policy = SimpleFinePolicy(per_day=10.0)
    lib = Library(policy)
    
    print("=== Library Management System ===")
    while True:
        print("\n1. Add Book  2. Add Member  3. Borrow  4. Return  5. Exit")
        choice = input("Select an option: ")

        try:
            if choice == "1":
                bid = input("Book ID: ")
                title = input("Title: ")
                author = input("Author: ")
                lib.add_book(bid, title, author)
                print("Book added successfully.")

            elif choice == "2":
                mid = input("Member ID: ")
                name = input("Name: ")
                lib.add_member(mid, name)
                print("Member registered.")

            elif choice == "3":
                mid = input("Member ID: ")
                bid = input("Book ID: ")
                lib.borrow_book(mid, bid, date.today())
                print(f"Book {bid} checked out to {mid}.")

            elif choice == "4":
                mid = input("Member ID: ")
                bid = input("Book ID: ")
                fine = lib.return_book(mid, bid, date.today())
                print(f"Book returned. Late fine: ${fine:.2f}")

            elif choice == "5":
                break
            else:
                print("Invalid choice.")

        except (ValueError, KeyError) as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()