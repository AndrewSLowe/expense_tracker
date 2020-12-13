import os
import sqlite3
import uuid
from typing import List
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field

class NotFound(Exception):
    pass

class Expense(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    amount: str
    created_at: str
    tags: str

    @classmethod
    def ListAll(cls) -> List['Expense']:
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("SELECT * FROM expenses")

        records = cur.fetchall()
        expenses = [cls(**record) for record in records] 

        conn.close()

        return expenses

    @classmethod
    def GetExpenseByID(cls, expense_id: str):
        """
        Query expenses by id (unique int)
        :param id:
        :return expenses:
        """
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row
    
        cur = conn.cursor()
        cur.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
        
        record = cur.fetchone()

        if record is None:
            return NotFound

        expense = cls(**record)
        conn.close()

        return expense

    def EditExpense(self, id) -> 'Expense':
        with sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db')) as conn:
            sql =  ''' 
                    UPDATE expenses 
                        SET title=?, 
                        amount=?, 
                        created_at=?, 
                        tags=?
                    WHERE id=?
                '''
                    
            values = (self.title, self.amount, self.created_at, self.tags, id)

            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return self

    def AddExpense(self) -> 'Expense':
        """
        Saves all listed expenses in the DB
        :param expenses => list:
        """
        with sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db')) as conn:
            sql = ''' INSERT INTO expenses (id, title, amount, created_at, tags)
            VALUES(?,?,?,?,?) '''
            values = (self.id, self.title, self.amount, self.created_at, self.tags)

            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return self

    @classmethod
    def create_table(cls, database_name='database.db'):
        """Create a table with the database_name statement"""

        conn = sqlite3.connect(database_name)
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS expenses (
                    id text,
                    title TEXT,
                    amount INT,
                    created_at TEXT,
                    tags TEXT
                ); """
        )
        conn.close()

def main():
    Expense.create_table()
    e1 = Expense(title='eggs', amount=12, created_at='12/01/20', tags='dairy')
    e2 = Expense(title='milk', amount=1, created_at='12/01/20', tags='groceries')
    e3 = Expense(title='cheese', amount=3, created_at='12/01/20', tags='gouda')
    e4 = Expense(title='yogurt', amount=1, created_at='12/01/20', tags='greek')

    e1.AddExpense()
    e2.AddExpense()
    e3.AddExpense()
    e4.AddExpense()
    
    Expense(title='yogurt', amount=1, created_at='12/01/20', tags='greek').EditExpense('e71c5fb5-6be7-49a6-852d-7c3063ecb6a1')
if __name__ == "__main__":
    main()