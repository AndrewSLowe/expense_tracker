# pylint: disable=no-name-in-module
from pydantic import BaseModel

from expenses.models import Expense, NotFound

class AlreadyExists(Exception):
    pass

class CreateExpenseCommand(BaseModel):
    title: str
    amount: str
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
    id: str
    title: str
    amount: str
    created_at: str
    tags: str

    def execute(self) -> Expense:
        expense = Expense(
            id = self.id,
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags
        ).EditExpense(self.id)

        return expense

def main():
    CreateExpenseCommand(title='milk', amount='3', created_at='yesterday', tags='plzwork').execute()
    EditExpenseCommand(id='833c86b0-dd0e-44ac-85c6-94a454d93be5',title='yoooo', amount='3', created_at='yesterday', tags='plzwork').execute()

if __name__ == "__main__":
    main()