import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the SQLite database or create it if it does not exist
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create the table to store expenses and income
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")

# Create the label for the amount entry
amount_label = ttk.Label(root, text="Amount:")
amount_label.grid(row=0, column=0)

# Create the entry for the amount
amount_entry = ttk.Entry(root)
amount_entry.grid(row=0, column=1)

# Create the label for the category
category_label = ttk.Label(root, text="Category:")
category_label.grid(row=1, column=0)

# Create the dropdown for the categories
categories = ["Food", "Auto", "Candy"]
category_var = tk.StringVar()
category_dropdown = ttk.OptionMenu(root, category_var, *categories)
category_dropdown.grid(row=1, column=1)

# Create the add button
def add_expense():
    amount = amount_entry.get()
    category = category_var.get()
    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, datetime('now'))", (amount, category))
    conn.commit()
    amount_entry.delete(0, tk.END)

add_button = ttk.Button(root, text="Add", command=add_expense)
add_button.grid(row=2, column=0, columnspan=2)

# Run the main loop
root.mainloop()
