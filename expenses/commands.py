# pylint: disable=no-name-in-module
from pydantic import BaseModel, EmailStr

from datetime import datetime
from expenses.models import Expense, Users, NotFound

class AlreadyExists(Exception):
    pass

class CreateExpenseCommand(BaseModel):
    title: str
    amount: float
    created_at: str
    tags: str
    email: EmailStr

    def execute(self) -> Expense:
        expense = Expense(
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags,
            email=self.email
        ).AddExpense()

        return expense

class EditExpenseCommand(BaseModel):
    id: str
    title: str
    amount: float
    created_at: str
    tags: str
    email: EmailStr

    def execute(self) -> Expense:
        expense = Expense(
            id=self.id,
            title=self.title,
            amount=self.amount,
            created_at=self.created_at,
            tags=self.tags,
            email=self.email
        ).EditExpense(id=self.id)

        return expense

class CreateNewUser(BaseModel):
    name: str
    password: str
    email: EmailStr
    created_at: datetime = datetime.now()

    def execute(self) -> Users:
        user = Users(
            name=self.name,
            password=self.password,
            email=self.email,
            created_at=self.created_at
        ).AddUser()

        return user


def main():
    CreateExpenseCommand(title='milk', amount=1, created_at='yesterday', tags='plzwork').execute()
    EditExpenseCommand(id=1, title='yoooo', amount=1, created_at='yesterday', tags='plzwork').execute()

if __name__ == "__main__":
    main()