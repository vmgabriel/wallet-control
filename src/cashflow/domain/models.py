from dataclasses import dataclass
from datetime import date as date_type
from uuid import uuid4, UUID

@dataclass
class Expense:
    id: UUID
    amount: float
    description: str
    category: str
    date: date_type

    @classmethod
    def create(cls, amount: float, description: str, category: str, date: date_type = None):
        return cls(
            id=uuid4(),
            amount=amount,
            description=description,
            category=category,
            date=date or date_type.today()
        )