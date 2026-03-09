# src/models.py
from typing import List, Dict
from abc import ABC, abstractmethod
from datetime import datetime

# Book Model
class Book:
    def __init__(self, book_id: int, title: str, available: bool = True):
        self.book_id = book_id
        self.title = title
        self.available = available

    def __str__(self):
        return f"Book ID: {self.book_id}, Title: {self.title}, Available: {self.available}"

# Member Model
class Member:
    def __init__(self, member_id: int, name: str):
        self.member_id = member_id
        self.name = name
        self.borrowed_books: List[int] = []  # List of book IDs

    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}, Borrowed Books: {self.borrowed_books}"

    def can_borrow(self) -> bool:
        return len(self.borrowed_books) < 3

# BorrowRecord Model
class BorrowRecord:
    def __init__(self, member: Member, book: Book, borrow_date: str):
        self.member = member
        self.book = book
        self.borrow_date = borrow_date
        self.returned = False

    def return_book(self):
        self.returned = True

# Fine Policy Interface
class FinePolicy(ABC):
    @abstractmethod
    def compute_fine(self, borrow_date: str, return_date: str) -> float:
        pass

# Concrete Fine Policy Implementation
class FinePolicyImpl(FinePolicy):
    def __init__(self, grace_period_days: int = 7, fine_per_day: float = 1.0):
        self.grace_period_days = grace_period_days
        self.fine_per_day = fine_per_day

    def compute_fine(self, borrow_date: str, return_date: str) -> float:
        borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d')
        return_date = datetime.strptime(return_date, '%Y-%m-%d')

        delta = return_date - borrow_date
        late_days = max((delta.days - self.grace_period_days), 0)
        fine = late_days * self.fine_per_day

        return fine

# Library Model
class Library:
    def __init__(self, fine_policy: FinePolicy):
        self.books: Dict[int, Book] = {}  # book_id -> Book
        self.members: Dict[int, Member] = {}  # member_id -> Member
        self.borrow_records: List[BorrowRecord] = []
        self.fine_policy = fine_policy

    def add_book(self, book: Book):
        if book.book_id in self.books:
            raise ValueError("Book with this ID already exists.")
        self.books[book.book_id] = book

    def add_member(self, member: Member):
        if member.member_id in self.members:
            raise ValueError("Member with this ID already exists.")
        self.members[member.member_id] = member

    def borrow_book(self, member_id: int, book_id: int, borrow_date: str):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            raise ValueError("Invalid member or book ID.")
        if not member.can_borrow():
            raise ValueError("Member cannot borrow more than 3 books.")
        if not book.available:
            raise ValueError("Book is not available for borrowing.")

        member.borrowed_books.append(book_id)
        book.available = False
        borrow_record = BorrowRecord(member, book, borrow_date)
        self.borrow_records.append(borrow_record)

    def return_book(self, member_id: int, book_id: int, return_date: str):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            raise ValueError("Invalid member or book ID.")
        if book.available:
            raise ValueError("Book was not borrowed.")
        if book_id not in member.borrowed_books:
            raise ValueError("This book was not borrowed by the member.")

        # Find the borrow record
        for record in self.borrow_records:
            if record.member == member and record.book == book and not record.returned:
                record.return_book()
                break
        
        member.borrowed_books.remove(book_id)
        book.available = True

        # Compute fine if necessary
        fine = self.fine_policy.compute_fine(borrow_date=record.borrow_date, return_date=return_date)
        return fine