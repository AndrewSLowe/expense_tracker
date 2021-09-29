import os
import sqlite3
import uuid
from typing import List
# pylint: disable=no-name-in-module
from pydantic import BaseModel, EmailStr, Field

import psycopg2

class NotFound(Exception):
    pass

class Expense(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    amount: float
    created_at: str
    tags: str
    email: EmailStr

    @classmethod
    def ListAll(cls):
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("SELECT * FROM expenses")

        records = cur.fetchall()
        expenses = [cls(**record) for record in records] 

        conn.close()

        return expenses

    @classmethod
    def GetExpenseByID(cls, id: int):
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

        expense = cls(**record)
        conn.close()

        return expense

    def AddExpense(self):
        """
        Saves all listed expenses in the DB
        :param expenses => list:
        """
        with sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db')) as conn:
            sql = ''' INSERT INTO expenses (title, amount, created_at, tags)
            VALUES(?,?,?,?) '''
            values = (self.title, self.amount, self.created_at, self.tags)

            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return self

    def EditExpense(self, id: int):
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

    @classmethod
    def create_table(cls):
        """Create a table with the database_name statement"""
        
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()

        cur.execute(
            """ CREATE TABLE IF NOT EXISTS expenses(
                    id TEXT,
                    title TEXT,
                    amount FLOAT,
                    created_at TEXT,
                    tags TEXT,
                    email TEXT
                ); """
        )
        cur.close()
        conn.commit()

    

class Users(BaseModel):
    name: str
    email: EmailStr

    def AddUser(self):
        """
        Saves all listed expenses in the DB
        :param expenses => list:
        """
        with sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db')) as conn:
            sql = ''' INSERT INTO users (name, email)
            VALUES(?,?) '''
            values = (self.name, self.email)

            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return self

    @classmethod
    def FindUserByEmail(cls, email: str):
        """
        Query expenses by id (unique int)
        :param id:
        :return expenses:
        """
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row
    
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))

        record = cur.fetchone()

        if record is None:
            return NotFound

        user = cls(**record)
        conn.close()

        return user

    @classmethod
    def create_table(cls):
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()

        cur.execute(
            """ CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    email TEXT
                ); """
        )
        cur.close()
        conn.commit()

def main():
    # Expense.create_table()
    # e1 = Expense(title='eggs', amount=12, created_at='12/08/1994', tags='dairy')
    # e2 = Expense(title='milk', amount=1, created_at='12/08/1994', tags='dairy')
    # e3 = Expense(title='cheese', amount=3, created_at='12/08/1994', tags='dairy')
    # e4 = Expense(title='yogurt', amount=1, created_at='12/08/1994', tags='dairy')

    # e1.AddExpense()
    # e2.AddExpense()
    # e3.AddExpense()
    # e4.AddExpense()

    # Expense(title='yogurt', amount=1, created_at='12/08/1994', tags='greek', id=1).EditExpense(1)

    Users.create_table()
    # Users(name="test", email="test@test.com").AddUser()
    print(Users.FindUserByEmail(email="test@test.com"))

if __name__ == "__main__":
    main()


    # pydantic pytest jsonschema flask pytest-cov requests psycopg2-binary jinja2 gunicorn