from pydantic import BaseModel, EmailStr

from models import Expense, NotFound

class AlreadyExists(Exception):
    pass

class CreateExpenseCommand(BaseModel):
    title: str
    amount: str
    created_at: str
    tags: str

    def execute(self) -> Expense:
        try:
            Expense.get_by_title(self.title)
            raise AlreadyExists
        except NotFound:
            pass

        expense = Expense(
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags
        ).AddExpense()

        return expense

class CreateEditExpenseCommand(BaseModel):
    pass

def main():
    CreateExpenseCommand(title='milk', amount='3', created_at='yesterday', tags='plzwork').execute()

if __name__ == "__main__":
    main()