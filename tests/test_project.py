import unittest
from datetime import date
from src.models import SimpleFinePolicy, Library

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.policy = SimpleFinePolicy(per_day=5.0)
        self.lib = Library(self.policy)
        self.lib.add_book("B1", "Python OOP", "Corey Schafer")
        self.lib.add_member("M1", "Alice")

    def test_successful_borrow(self):
        self.lib.borrow_book("M1", "B1", date(2023, 1, 1))
        self.assertFalse(self.lib.books["B1"].is_available())
        self.assertIn("B1", self.lib.members["M1"].borrow_books)

    def test_borrow_unavailable_book(self):
        self.lib.borrow_book("M1", "B1", date(2023, 1, 1))
        # Second member tries to borrow same book
        self.lib.add_member("M2", "Bob")
        with self.assertRaises(ValueError):
            self.lib.borrow_book("M2", "B1", date(2023, 1, 2))

    def test_borrow_limit_reached(self):
        self.lib.add_book("B2", "Title 2", "Author")
        self.lib.add_book("B3", "Title 3", "Author")
        self.lib.add_book("B4", "Title 4", "Author")
        
        self.lib.borrow_book("M1", "B1", date(2023, 1, 1))
        self.lib.borrow_book("M1", "B2", date(2023, 1, 1))
        self.lib.borrow_book("M1", "B3", date(2023, 1, 1))
        
        # 4th book should fail (Limit is 3)
        with self.assertRaises(ValueError):
            self.lib.borrow_book("M1", "B4", date(2023, 1, 1))

    def test_fine_calculation_grace_period(self):
        self.lib.borrow_book("M1", "B1", date(2023, 1, 1))
        # Returned on day 7 (within grace period)
        fine = self.lib.return_book("M1", "B1", date(2023, 1, 8))
        self.assertEqual(fine, 0.0)

    def test_fine_calculation_late(self):
        self.lib.borrow_book("M1", "B1", date(2023, 1, 1))
        # Returned on day 10 (3 days late: 10 - 7 = 3)
        # 3 days * 5.0 = 15.0
        fine = self.lib.return_book("M1", "B1", date(2023, 1, 11))
        self.assertEqual(fine, 15.0)

    def test_return_unborrowed_book(self):
        with self.assertRaises(ValueError):
            self.lib.return_book("M1", "B1", date(2023, 1, 5))

    def test_invalid_member_id(self):
        with self.assertRaises(KeyError):
            self.lib.borrow_book("INVALID", "B1", date(2023, 1, 1))

    def test_duplicate_book_id(self):
        with self.assertRaises(ValueError):
            self.lib.add_book("B1", "Duplicate", "Author")

if __name__ == "__main__":
    unittest.main()