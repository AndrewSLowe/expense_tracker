# Build expense tracker CLI app.

# Each expense should have following attributes:
# * title (string)
# * amount (float)
# * created_at (date)
# * tags (list of strings)

# Store expenses in TXT file.

# Cover: Add expense, list expenses, get expense, edit expense, delete expense

import os

def addExpense(title, amount, created_at, tags):
    new_line = title + '  ' + amount + '  ' + created_at + '  ' + tags + '\n'
    file_object = open("expenses.txt", "a")
    file_object.write(new_line)
    file_object.close()

def listExpenses():
    file_object = open("expenses.txt", "r")
    print(file_object.read()[:-1])
    file_object.close()

def getExpense(expense):

    file_object = open("expenses.txt")

    for line in file_object:
        item = line.split("  ")[0]
        if item == expense:
            print(line[:-1])
        
def editExpense(expense):
    file_object = open("expenses.txt", "r")
    lines = ""

    for line in file_object:
        items = line.split("  ")
        if items[0] == expense:

            x = input('Value to edit: ')

            if x == 'amount':
                items[1] = input('Amount: ')
            if x == 'created_at':
                items[2] = input('Created at: ')
            if x == 'tags':
                items[3] = input('Tags: ')

            line = "  ".join(map(str, items)) +'\n'

        lines += line
    
    writing_file = open("expenses.txt", "w")
    writing_file.write(lines)
    writing_file.close()

def deleteExpense(expense):
    file_object = open("expenses.txt", "r")
    lines = ""

    for line in file_object:
        items = line.split("  ")
        if items[0] == expense:
            pass
        else:
            lines += line
    
    writing_file = open("expenses.txt", "w")
    writing_file.write(lines)
    writing_file.close()

if __name__ == "__main__":
    addExpense('eggs', '12', '2pm', 'mks;ang')
    addExpense('milk', '5', '3pm', 'dairy')
    addExpense('cheese', '1', '4pm', 'groceries')
    # deleteExpense('rere')
    listExpenses()
    