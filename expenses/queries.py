from typing import List
from pydantic import BaseModel
from models import Expense, NotFound

class ListExpensesQuery(BaseModel):

    def execute(self) -> List[Expense]:
        expenses = Expense.ListAll()

        return expenses
    
class GetByIDQuery(BaseModel):
    def execute(self, id: str):
        expenses = Expense.GetByID(id)

        return expenses

def main():
    print(ListExpensesQuery().execute())
    print('==================')
    print(GetByIDQuery().execute('e71c5fb5-6be7-49a6-852d-7c3063ecb6a1'))

if __name__ == "__main__":
    main()