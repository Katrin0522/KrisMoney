import customtkinter
import tkinter.ttk as ttk
from tkinter import messagebox
import random
import sqlite3
from tkcalendar import DateEntry
conn = sqlite3.connect('income.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS income_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date text,
                category text,
                amount real
                )""")

c.execute("""CREATE TABLE IF NOT EXISTS outcome_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date text,
                category text,
                amount real
                )""")

c.execute("""CREATE TABLE IF NOT EXISTS category_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text)""")

c.execute("""CREATE TABLE IF NOT EXISTS duty_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date text,
                people text,
                description text,
                amount real
                )""")

customtkinter.set_appearance_mode('dark')
class KrisMoney(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Конфигурация
        self.title("KrisMoney - Мониторинг хорошего настроения")
        self.geometry(f"{800}x{500}")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # Стили
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TableStyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        self.style.configure("TableStyle.Treeview", background="#bebcb9", fieldbackground="#bebcb9", foreground="black")
        self.style.configure("TableStyle.Treeview.Heading", background="#bebcb9", fieldbackground="#bebcb9", foreground="black", relief="flat")
        self.style.configure("TableStyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        self.style.layout("TableStyle.Treeview", [('TableStyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        # Боковое меню
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_main_block, text="Главное", width=80)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_income_block, text="Доходы", width=80)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_outcome_block, text="Расходы", width=80)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_duty_block, text="Долги", width=80)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_category_block, text="Категории", width=80)
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        
        # Главный блок
        self.main_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.main_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        self.title_text = customtkinter.CTkLabel(self.main_block, text="Главное")
        self.title_text.pack()
        self.income_text = customtkinter.CTkLabel(self.main_block, text="0")
        self.income_text.pack(side="left")

        # self.outcome_text = customtkinter.CTkLabel(self.main_block, text="Последние расходы")
        # self.outcome_text.pack(side="right")

        # Доходный блок
        self.income_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.income_block, text="Доходы")
        self.title_text.pack()

        self.frame_table_income = customtkinter.CTkFrame(self.income_block)
        self.frame_table_income.pack(side="top")
            # Таблица 
        columns = ("1", "2", "3", "4")
        self.income_Table = ttk.Treeview(self.frame_table_income, show="headings", columns=columns, style="TableStyle.Treeview")
        self.income_Table.heading("1", text="#")
        self.income_Table.heading("2", text="Дата")
        self.income_Table.heading("3", text="Источник")
        self.income_Table.heading("4", text="Сумма")
        self.scrolltable = customtkinter.CTkScrollbar(self.frame_table_income, command=self.income_Table.yview)
        self.income_Table.configure(yscrollcommand=self.scrolltable.set)
        self.scrolltable.pack(side="right", fill="y")
        self.income_Table.pack(fill="both", expand=1)

        self.add_income = customtkinter.CTkButton(self.income_block, text="Добавить", command=self.show_input_window_income)
        self.add_income.pack(side="left")

        self.delete_income = customtkinter.CTkButton(self.income_block, text="Удалить", command=self.delete_record)
        self.delete_income.pack(side="right")

        # Расходный блок
        self.outcome_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.outcome_block, text="Расходы")
        self.title_text.pack()

        # Долговой блок
        self.duty_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.duty_block, text="Долги")
        self.title_text.pack()

        # Категории блок
        self.category_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.category_block, text="Категории")
        self.title_text.pack()

    def only_numbers(self, char):
        if char.isdigit() or char == ".":
            return True
        else:
            return False

    # Кнопки бокового меню
    def button_callback(self):
        print("button pressed")

    def button_main_block(self):
        if self.income_block.winfo_ismapped():
            self.income_block.grid_forget()
            self.reflesh_balance()
            self.main_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.outcome_block.winfo_ismapped():
            self.outcome_block.grid_forget()
            self.main_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.duty_block.winfo_ismapped():
            self.duty_block.grid_forget()
            self.main_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.category_block.winfo_ismapped():
            self.category_block.grid_forget()
            self.main_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

    def button_income_block(self):
        if self.main_block.winfo_ismapped():
            self.main_block.grid_forget()
            self.refresh_tree_income()
            self.income_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.outcome_block.winfo_ismapped():
            self.outcome_block.grid_forget()
            self.refresh_tree_income()
            self.income_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.duty_block.winfo_ismapped():
            self.duty_block.grid_forget()
            self.refresh_tree_income()
            self.income_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.category_block.winfo_ismapped():
            self.category_block.grid_forget()
            self.refresh_tree_income()
            self.income_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

    def button_outcome_block(self):
        if self.main_block.winfo_ismapped():
            self.main_block.grid_forget()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.income_block.winfo_ismapped():
            self.income_block.grid_forget()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.duty_block.winfo_ismapped():
            self.duty_block.grid_forget()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.category_block.winfo_ismapped():
            self.category_block.grid_forget()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

    def button_duty_block(self):
        if self.main_block.winfo_ismapped():
            self.main_block.grid_forget()
            self.duty_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.outcome_block.winfo_ismapped():
            self.outcome_block.grid_forget()
            self.duty_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.income_block.winfo_ismapped():
            self.income_block.grid_forget()
            self.duty_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.category_block.winfo_ismapped():
            self.category_block.grid_forget()
            self.duty_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

    def button_category_block(self):
        if self.main_block.winfo_ismapped():
            self.main_block.grid_forget()
            self.category_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.outcome_block.winfo_ismapped():
            self.outcome_block.grid_forget()
            self.category_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.income_block.winfo_ismapped():
            self.income_block.grid_forget()
            self.category_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.duty_block.winfo_ismapped():
            self.duty_block.grid_forget()
            self.category_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

    def save_input(self):
        global entered_text
        self.first_entry = self.date_enter_income.get()
        self.two_entry = self.source_enter_income.get()
        self.three_entry = self.sum_enter_income.get()

        if not self.first_entry or not self.two_entry or not self.three_entry:
            messagebox.showerror("Ошибка", "Не все поля заполнены")
            self.input_window.focus_force()
            return

        self.enter_incomebase = [self.first_entry, self.two_entry, self.three_entry]

        c.execute("INSERT INTO income_table (date, category, amount) VALUES (?, ?, ?)", (self.enter_incomebase[0], self.enter_incomebase[1], self.enter_incomebase[2]))
        conn.commit()
        self.refresh_tree_income()
        self.input_window.destroy()

    def refresh_tree_income(self):
        self.income_Table.delete(*self.income_Table.get_children())
        c.execute("SELECT * FROM income_table")
        data_income = c.fetchall()
        print(data_income)
        data_income.reverse()
        for row in data_income:
            self.income_Table.insert("", "end", values=row)

    # Кнопка вызова окна для добавления новой записи дохода
    def show_input_window_income(self):
        self.input_window = customtkinter.CTkToplevel()
        self.input_window.title("Добавление записи")
        self.input_window.geometry(f"{300}x{200}")
        self.input_window.grab_set()

        # Сюда выбор даты вставлять
        self.first_name_label = customtkinter.CTkLabel(self.input_window, text="Дата:", width=100)
        self.first_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.date_enter_income = DateEntry(self.input_window, width=20, background='blue', foreground="white", borderwidth=2, year=2023, locale="ru_RU")
        self.date_enter_income.grid(row=0, column=1, padx=10, pady=10)

        self.last_name_label = customtkinter.CTkLabel(self.input_window, text="Источник:", width=100)
        self.last_name_label.grid(row=1, column=0, padx=10, pady=10)
        self.source_enter_income = customtkinter.CTkEntry(self.input_window)
        self.source_enter_income.grid(row=1, column=1, padx=10, pady=10)

        # Сюда проверку на цифры сунуть
        self.age_label = customtkinter.CTkLabel(self.input_window, text="Сумма:", width=100)
        self.age_label.grid(row=2, column=0, padx=10, pady=10)
        self.sum_enter_income = customtkinter.CTkEntry(self.input_window)
        self.sum_enter_income.configure(validate="key", validatecommand=(self.register(self.only_numbers), "%S"))
        self.sum_enter_income.grid(row=2, column=1, padx=10, pady=10)

        self.submit_button = customtkinter.CTkButton(self.input_window, text="Подтвердить", command=self.save_input, width=50)
        self.submit_button.grid(row=3, column=0, padx=10, pady=10)

        self.dismit_button = customtkinter.CTkButton(self.input_window, text="Отмена", command=self.input_window.destroy, width=50)
        self.dismit_button.grid(row=3, column=1, padx=10, pady=10)

    def delete_record(self):
        selected_item = self.income_Table.focus()
        self.income_Table.delete(selected_item)

    def reflesh_balance(self):
        c.execute("SELECT * FROM income_table")
        balance = 0
        for row in c.fetchall():
            balance += row[2]

        print(balance)
        self.income_text.configure(text = "Баланс: "+str(balance))
if __name__ == "__main__":
    app = KrisMoney()
    app.mainloop()