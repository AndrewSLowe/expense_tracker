from typing import List
from pydantic import BaseModel
from models import Expense, NotFound

class ListExpensesQuery(BaseModel):

    def execute(self) -> List[Expense]:
        expenses = Expense.ListAll()

        return expenses
    
class ListArticlesQuery(BaseModel):
    def execute(self, id: str):
        expenses = Expense.GetByID(id)

        return expenses

def main():
    print(ListExpensesQuery().execute())

if __name__ == "__main__":
    main()