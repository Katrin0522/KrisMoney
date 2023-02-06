import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

conn = sqlite3.connect("income_expense.db")
c = conn.cursor()

current_datetime = datetime.now()
data_now = current_datetime.date()
aa = False
c.execute("CREATE TABLE IF NOT EXISTS finance (date_record text, category text, amount real)")

def add_income(amount):
    current_datetime = datetime.now()
    data_now = current_datetime
    c.execute("INSERT INTO finance (date_record, category, amount) VALUES (?, ?, ?)", (data_now, 'income', amount))
    conn.commit()
    show_records()

def add_expense(amount):
    current_datetime = datetime.now()
    data_now = current_datetime.date()
    c.execute("INSERT INTO finance (date_record, category, amount) VALUES (?, ?, ?)", (data_now, 'expense', amount))
    conn.commit()
    show_records()

def show_records():
    global aa
    if aa == True:
        selected_item = tree.selection()[0] ## get selected item
        print(selected_item)
        tree.delete(selected_item)
    c.execute("SELECT * FROM finance")
    records = c.fetchall()
    for i, record in enumerate(records):
        print(i, record)
        # for j, item in enumerate(record):
        #     print(record)
        tree.insert("", i, values=record)
    aa = True


def clear_records():
    c.execute("DELETE FROM finance")
    conn.commit()
    show_records()

root = tk.Tk()
root.title("Income/Expense Tracker")
root.geometry("1280x800")

frame = ttk.Frame(root)
frame.pack(pady=20)

income_label = ttk.Label(frame, text="Income:")
income_label.grid(row=0, column=0, padx=10, pady=10)

income_entry = ttk.Entry(frame)
income_entry.grid(row=0, column=1, padx=10, pady=10)

add_income_button = ttk.Button(frame, text="Add Income", command=lambda: add_income(income_entry.get()))
add_income_button.grid(row=0, column=2, padx=10, pady=10)

expense_label = ttk.Label(frame, text="Expense:")
expense_label.grid(row=1, column=0, padx=10, pady=10)

expense_entry = ttk.Entry(frame)
expense_entry.grid(row=1, column=1, padx=10, pady=10)

add_expense_button = ttk.Button(frame, text="Add Expense", command=lambda: add_expense(expense_entry.get()))
add_expense_button.grid(row=1, column=2, padx=10, pady=10)

tree = ttk.Treeview(root, columns=("date_record", "category", "amount"))
tree.pack(pady=20, expand=1)

root.mainloop()