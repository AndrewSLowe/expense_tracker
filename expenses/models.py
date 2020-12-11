import os
import sqlite3
import uuid
from typing import List

from pydantic import BaseModel, EmailStr, Field

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
    def GetByID(cls, id: str):
        """
        Query expenses by id (unique int)
        :param id:
        :return expenses:
        """
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row
    
        cur = conn.cursor()
        cur.execute("SELECT * FROM expenses WHERE id=?", (id,))
        record = cur.fetchone()

        if record is None:
            return NotFound

        expenses = cls(**record)
        conn.close()

        return expenses

    def EditExpense(self) -> 'Expense':
        pass

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
                    title VARCHAR(64),
                    amount VARCHAR(64),
                    created_at VARCHAR,
                    tags VARCHAR
                ); """
        )
        conn.close()

def main():
    Expense.create_table()

if __name__ == "__main__":
  main()