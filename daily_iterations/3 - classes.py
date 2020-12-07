import sqlite3
from sqlite3 import Error

# Database functions
def create_connection(db_file):
    """ 
    create a database connection to the SQLite database
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
    """ 
    Create a table with the create_table_sql statement

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

# Expense class
class Expense:
    def __init__(self, title, amount, created_at, tags=[]):
        self.title = title
        self.amount = amount
        self.created_at = created_at
        self.tags = tags

# Expense repo (connects to db)
class ExpenseRepository:
    def __init__(self, db_file):
        self.table_name = db_file[:-3]
        self.conn = create_connection(db_file)

    def save(self, expenses):
        """
        Saves all listed expenses in the DB
        :param expenses => list:
        """
        if isinstance(expenses, list) is False:
            expenses = [expenses]
        
        for i in expenses:
            entry = (i.title, i.amount, i.created_at, i.tags)
            create_expense(self.conn, entry)

    def get_by_id(self, expense_id):
        """
        Query expenses by expense_id (unique int)
        :param expense_id:
        :return:
        """
        cur = self.conn.cursor()
        query = "SELECT * FROM " + self.table_name + "WHERE expense_id=?"
        cur.execute(query, (expense_id,))
        rows = cur.fetchall()

        for row in rows:
            print(row)

    def _list(self):
        """
        Query all expenses
        :return:
        """
        cur = self.conn.cursor()
        query = "SELECT * FROM " + self.table_name
        cur.execute(query)
        rows = cur.fetchall()

        for row in rows:
            print(row)

    def delete(self, expense_id):
        """
        Query expenses by expense_id (unique int)
        :param expense_id:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))

def main():
    database = "expenses.db"

    sql_create_expenses_table = """ CREATE TABLE IF NOT EXISTS expenses (
                                        expense_id INTEGER PRIMARY KEY,
                                        title VARCHAR(64),
                                        amount int NOT NULL,
                                        created_at DATE,
                                        tags VARCHAR
                                    ); """

    # create a database object
    ER = ExpenseRepository(database)
    # create tables
    if ER.conn is not None:
        # create expense table
        create_table(ER.conn, sql_create_expenses_table)
    else:
        print("Error! cannot create the database connection.")

    with ER.conn:
        # create a new expense
        ex1 = Expense('eggs', '5', '12-05-2020', 'groceries')
        ex2 = Expense('milk', '2', '12-05-2020', 'dairy')
        ex3 = Expense('cheese', '9', '12-05-2020', 'groceries')

        ER.save([ex1, ex2, ex3])

        ER.delete(4)
        ER.delete(5)
        ER._list()

if __name__ == "__main__":
    main()