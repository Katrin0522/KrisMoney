import tkinter as tk

def show_input_window():
    input_window = tk.Toplevel()
    input_window.title("Input Data")

    first_name_label = tk.Label(input_window, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=10, pady=10)
    first_name_entry = tk.Entry(input_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    last_name_label = tk.Label(input_window, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=10, pady=10)
    last_name_entry = tk.Entry(input_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    age_label = tk.Label(input_window, text="Age:")
    age_label.grid(row=2, column=0, padx=10, pady=10)
    age_entry = tk.Entry(input_window)
    age_entry.grid(row=2, column=1, padx=10, pady=10)

    submit_button = tk.Button(input_window, text="Submit", command=input_window.destroy)
    submit_button.grid(row=3, column=1, padx=10, pady=10)

root = tk.Tk()
root.title("Main Window")

open_input_window_button = tk.Button(root, text="Open Input Window", command=show_input_window)
open_input_window_button.pack(pady=20)

root.mainloop()


# Подтврерждение что всё заполнено
# import tkinter as tk
# from tkinter import messagebox

# def submit_data():
#     name = entry1.get()
#     age = entry2.get()
#     city = entry3.get()
#     if not name or not age or not city:
#         messagebox.showerror("Error", "All fields are required")
#         return
#     messagebox.showinfo("Success", "Data submitted successfully")

# root = tk.Tk()
# root.geometry("300x200")
# root.title("Data Entry")

# label1 = tk.Label(root, text="Name")
# label2 = tk.Label(root, text="Age")
# label3 = tk.Label(root, text="City")

# entry1 = tk.Entry(root)
# entry2 = tk.Entry(root)
# entry3 = tk.Entry(root)

# label1.grid(row=0, column=0, pady=10)
# label2.grid(row=1, column=0, pady=10)
# label3.grid(row=2, column=0, pady=10)

# entry1.grid(row=0, column=1, pady=10)
# entry2.grid(row=1, column=1, pady=10)
# entry3.grid(row=2, column=1, pady=10)

# submit_button = tk.Button(root, text="Submit", command=submit_data)
# submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# root.mainloop()
