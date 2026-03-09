# Library Management System (OOP)

## Project Description
This is a robust, object-oriented Library Management System built with Python. It manages a catalog of books and a database of members, handling borrowing and return workflows while strictly enforcing business rules such as borrow limits and late fine calculations.

## OOP Concepts Applied
To meet the project requirements, the following core principles were implemented:
*   **Encapsulation**: Book availability (`__available`) and member borrowed lists (`__borrowed_books`) are private. They can only be modified through validated methods like `borrow()` and `return_book()`.
*   **Abstraction**: A `FinePolicy` Abstract Base Class (ABC) defines the interface for all fine calculations, hidden from the main Library logic.
*   **Polymorphism**: The `Library` class accepts any implementation of `FinePolicy`. Currently, it uses `SimpleFinePolicy`, but others can be swapped in without changing the core code.
*   **Composition**: The `Library` class acts as a container that "has" collections of `Book`, `Member`, and `BorrowRecord` objects.
*   **Separation of Concerns**: Business logic is strictly contained in `src/`, while user interaction is handled separately in `cli.py`.

## How to Run the Program
1. Ensure you have Python 3.7+ installed.
2. Navigate to the project root directory.
3. Run the CLI application:
   ```bash
   python cli.py