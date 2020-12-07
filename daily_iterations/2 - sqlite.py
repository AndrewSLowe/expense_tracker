# Add database

# Instead to storing/reading in/from TXT file start using SQLite.

# Write script to copy all of the existing expenses from TXT file to database.

# Don't use ORM at this point.
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_expense(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO expenses (title, amount, created_at, tags)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def load_txt_file(conn, txtFile):
    
    file_object = open(txtFile)

    for line in file_object:
        expense = tuple(line.split("  "))
        create_expense(conn, expense)

def main():
    database = "expenses.db"

    # title (string)
    # amount (float)
    # created_at (date)
    # tags (list of strings)

    sql_create_expenses_table = """ CREATE TABLE IF NOT EXISTS expenses (
                                        expense_id INTEGER PRIMARY KEY,
                                        title text,
                                        amount int NOT NULL,
                                        created_at text,
                                        tags text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create expense table
        create_table(conn, sql_create_expenses_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new expense
        project = ('eggs', 15, '2015-01-01', 'groceries')
        create_expense(conn, project)

        load_txt_file(conn, 'expenses.txt')

if __name__ == "__main__":
    main()