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
        expense = Expense(
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags
        ).AddExpense()

        return expense

class CreateEditExpenseCommand(BaseModel):
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
    id = '682e211c-f736-4063-ba42-ec8cf297fcc4'
    CreateExpenseCommand(title='milk', amount='3', created_at='yesterday', tags='plzwork').execute()
    CreateEditExpenseCommand(title='milk', amount='3', created_at='yesterday', tags='plzwork').execute(id)

if __name__ == "__main__":
    main()