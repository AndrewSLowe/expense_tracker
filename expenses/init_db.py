from expenses.models import Expense, Users

if __name__=="__main__":
    Expense.create_table()
    Users.create_table()