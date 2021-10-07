from datetime import datetime
import os
import sqlite3
import uuid
from typing import List
# pylint: disable=no-name-in-module
from pydantic import BaseModel, EmailStr, Field

from psycopg2.extras import RealDictCursor
import psycopg2

DEFAULT_DB = os.getenv('DATABASE_URL')

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
        conn = psycopg2.connect(os.getenv('DATABASE_NAME', DEFAULT_DB))
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM expenses WHERE email=%s", (email,))

        records = cur.fetchall()
        expenses = [cls(**record) for record in records] 

        cur.close()
        conn.commit()

        return expenses

    @classmethod
    def GetExpenseByID(cls, id: str, email: EmailStr):
        """
        Query expenses by id (unique uuid)
        :param id:
        :return expense:
        """
        conn = psycopg2.connect(os.getenv('DATABASE_NAME', DEFAULT_DB))
    
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
        with psycopg2.connect(os.getenv('DATABASE_NAME', DEFAULT_DB)) as conn:
            sql = ''' INSERT INTO expenses (id, title, amount, created_at, tags, email)
            VALUES(%s, %s, %s, %s, %s, %s) '''
            values = (self.id, self.title, self.amount, self.created_at, self.tags, self.email)

            cur = conn.cursor()
            cur.execute(sql, values)
            cur.close()
            conn.commit()

        return self

    def EditExpense(self, id: str):
        with psycopg2.connect(os.getenv('DATABASE_NAME', DEFAULT_DB)) as conn:
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
    def create_table(cls, database_name=os.getenv('DATABASE_URL')):
        """Create a table with the database_name statement"""
        
        conn = psycopg2.connect(database_name)
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

    @classmethod
    def drop_table(cls, database_name=os.getenv('DATABASE_URL')):
        conn = psycopg2.connect(database_name)
        cur = conn.cursor()

        cur.execute(
            """ TRUNCATE TABLE expenses CASCADE; """
        )
        cur.close()
        conn.commit()

    

class Users(BaseModel):
    name: str
    password: str
    email: EmailStr
    created_at: datetime = None
    active: bool = True

    def AddUser(self):
        """
        Saves all listed expenses in the DB
        :param expenses => list:
        """
        with psycopg2.connect(os.getenv('DATABASE_NAME', DEFAULT_DB)) as conn:

            self.created_at = datetime.now()   #.strftime("%m/%d/%Y, %H:%M:%S")

            sql = ''' INSERT INTO users (name, password, email, created_at, active)
            VALUES(%s, %s, %s, %s, %s) '''
            values = (self.name, self.password, self.email, self.created_at, self.active)

            cur = conn.cursor()
            cur.execute(sql, values)
            cur.close()
            conn.commit()
            

        return self

    @classmethod
    def GetUserByEmail(cls, email: EmailStr):
        """
        Query expenses by id (unique uuid)
        :param id:
        :return expense:
        """
        conn = psycopg2.connect(os.getenv('DATABASE_NAME', DEFAULT_DB))
    
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))

        record = cur.fetchone()

        if record is None:
            return NotFound

        user = cls(**record)
        conn.close()

        return user

    @classmethod
    def create_table(cls, database_name=os.getenv('DATABASE_URL')):
        conn = psycopg2.connect(database_name)
        cur = conn.cursor()

        cur.execute(
            """ CREATE TABLE IF NOT EXISTS users(
                    name TEXT,
                    password TEXT,
                    email TEXT,
                    created_at TIMESTAMP,
                    active BOOL
                ); """
        )
        cur.close()
        conn.commit()

    @classmethod
    def drop_table(cls, database_name=os.getenv('DATABASE_URL')):
        conn = psycopg2.connect(database_name)
        cur = conn.cursor()
        cur.execute(
            """ TRUNCATE TABLE users CASCADE; """
        )
        cur.close()
        conn.commit()
