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

def main():
    print(ListExpensesQuery().execute())
    print('==================')
    print(GetExpenseByIDQuery(id=1).execute())
    print(GetExpenseByIDQuery(id=16).execute())

if __name__ == "__main__":
    main()