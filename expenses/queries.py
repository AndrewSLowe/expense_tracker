from typing import List
# pylint: disable=no-name-in-module
from pydantic import BaseModel, EmailStr
from expenses.models import Expense, NotFound, Users

class ListExpensesQuery(BaseModel):
    email: EmailStr

    def execute(self) -> List[Expense]:
        expenses = Expense.ListAll(self.email)

        return expenses
    
class GetExpenseByIDQuery(BaseModel):
    id: str
    email: EmailStr

    def execute(self) -> Expense:
        expense = Expense.GetExpenseByID(self.id, self.email)

        return expense

class GetUserByEmailQuery(BaseModel):
    email: EmailStr

    def execute(self) -> Users:
        user = Users.GetUserByEmail(self.email)

        return user