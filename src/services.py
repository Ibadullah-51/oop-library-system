# src/services.py
from abc import ABC, abstractmethod
from datetime import datetime

class FinePolicy(ABC):
    @abstractmethod
    def compute_fine(self, borrow_date: str, return_date: str) -> float:
        pass

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