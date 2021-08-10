# pylint: disable=no-name-in-module
from pydantic import BaseModel

from expenses.models import Expense, NotFound

class AlreadyExists(Exception):
    pass

class CreateExpenseCommand(BaseModel):
    title: str
    amount: float
    created_at: str
    tags: str

    def execute(self) -> Expense:
        expense = Expense(
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags
        ).AddExpense()

        return expense

class EditExpenseCommand(BaseModel):
    id: int
    title: str
    amount: float
    created_at: str
    tags: str

    def execute(self) -> Expense:
        expense = Expense(
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags
        ).EditExpense(id=self.id)

        return expense

def main():
    CreateExpenseCommand(title='milk', amount=1, created_at='yesterday', tags='plzwork').execute()
    EditExpenseCommand(id=1, title='yoooo', amount=1, created_at='yesterday', tags='plzwork').execute()

if __name__ == "__main__":
    main()