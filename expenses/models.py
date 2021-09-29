import os
import sqlite3
import uuid
from typing import List
# pylint: disable=no-name-in-module
from pydantic import BaseModel, EmailStr, Field

from psycopg2.extras import RealDictCursor
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
    def ListAll(cls, email: str):
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM expenses WHERE email=%s", (email,))

        records = cur.fetchall()
        expenses = [cls(**record) for record in records] 

        cur.close()
        conn.commit()

        return expenses

    @classmethod
    def GetExpenseByID(cls, id: str, email: str):
        """
        Query expenses by id (unique int)
        :param id:
        :return expenses:
        """
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM expenses WHERE id=%s AND email=%s", (id, email))

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
        with psycopg2.connect(os.environ.get('DATABASE_URL')) as conn:
            sql = ''' INSERT INTO expenses (id, title, amount, created_at, tags, email)
            VALUES(%s, %s, %s, %s, %s, %s) '''
            values = (self.id, self.title, self.amount, self.created_at, self.tags, self.email)

            cur = conn.cursor()
            cur.execute(sql, values)
            cur.close()
            conn.commit()

        return self

    def EditExpense(self, id: str):
        with psycopg2.connect(os.environ.get('DATABASE_URL')) as conn:
            sql =  ''' 
                    UPDATE expenses 
                        SET title=%s, 
                        amount=%s, 
                        created_at=%s, 
                        tags=%s
                    WHERE id=%s
                        AND email=%s
                '''
                    
            values = (self.title, self.amount, self.created_at, self.tags, id, self.email)

            cur = conn.cursor()
            cur.execute(sql, values)
            cur.close()
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
        with psycopg2.connect(os.environ.get('DATABASE_URL')) as conn:
            sql = ''' INSERT INTO users (name, email)
            VALUES(%s, %s) '''
            values = (self.name, self.email)

            cur = conn.cursor()
            cur.execute(sql, values)
            cur.close()
            conn.commit()
            

        return self

    @classmethod
    def FindUserByEmail(cls, email: str):
        """
        Query expenses by id (unique int)
        :param id:
        :return expenses:
        """
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))

        record = cur.fetchone()

        if record is None:
            return NotFound

        user = cls(**record)
        cur.close()
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