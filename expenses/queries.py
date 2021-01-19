from typing import List
# pylint: disable=no-name-in-module
from pydantic import BaseModel
from expenses.models import Expense, NotFound

class ListExpensesQuery(BaseModel):

    def execute(self) -> List[Expense]:
        expenses = Expense.ListAll()

        return expenses
    
class GetExpenseByIDQuery(BaseModel):
    id: int

    def execute(self) -> Expense:
        expense = Expense.GetExpenseByID(self.id)

        return expense

def main():
    print(ListExpensesQuery().execute())
    print('==================')
    print(GetExpenseByIDQuery(id=1).execute())
    print(GetExpenseByIDQuery(id=16).execute())

if __name__ == "__main__":
    main()