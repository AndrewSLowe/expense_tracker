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
    title: str
    amount: str
    created_at: str
    tags: str

    def execute(self, id) -> Expense:
        expense = Expense(
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags
        ).EditExpense(id)

        return expense

def main():
    id = 'e875b8ed-0757-4dc4-a770-86050e15b8d4'
    CreateExpenseCommand(title='milk', amount='3', created_at='yesterday', tags='plzwork').execute()
    CreateEditExpenseCommand(title='milk', amount='3', created_at='yesterday', tags='plzwork').execute(id)

if __name__ == "__main__":
    main()