from cashflow.domain.models import Expense
from cashflow.domain.repositories import ExpenseRepository

class ExpenseService:
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    def record_expense(self, amount: float, description: str, category: str):
        expense = Expense.create(amount, description, category)
        self.repo.add(expense)
        return expense

    def get_summary(self):
        expenses = self.repo.get_all()
        total = self.repo.get_balance()
        return {
            "total_expenses": total,
            "count": len(expenses),
            "last_movements": expenses[:5]
        }