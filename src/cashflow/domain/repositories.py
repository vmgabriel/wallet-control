from abc import ABC, abstractmethod
from typing import List
from .models import Expense

class ExpenseRepository(ABC):
    @abstractmethod
    def add(self, expense: Expense) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Expense]:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass