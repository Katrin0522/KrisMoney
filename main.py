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
        self.my_font = customtkinter.CTkFont(family="Arial 14 bold")

        # Стили
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TableStyle.Treeview", highlightthickness=0, bd=0,font=('Calibri', 11)) # Modify the font of the body
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
        self.income_Table = ttk.Treeview(self.frame_table_income, show="headings", columns=columns, style="TableStyle.Treeview", height=18)
        self.income_Table.heading("1", text="#")
        self.income_Table.heading("2", text="Дата")
        self.income_Table.heading("3", text="Источник")
        self.income_Table.heading("4", text="Сумма")
        self.income_Table.column("2", width=84, anchor="center", minwidth=84)
        self.scrolltable = customtkinter.CTkScrollbar(self.frame_table_income, command=self.income_Table.yview)
        self.income_Table.configure(yscrollcommand=self.scrolltable.set)
        self.scrolltable.pack(side="right", fill="y")
        self.income_Table.pack(fill="both", expand=True)
        self.add_income = customtkinter.CTkButton(self.income_block, text="Добавить", command=self.show_input_window_income)
        self.add_income.pack(side="left")

        self.delete_income = customtkinter.CTkButton(self.income_block, text="Удалить", command=self.delete_record)
        self.delete_income.pack(side="right")

        # Расходный блок
        self.outcome_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.outcome_block, text="Расходы")
        self.title_text.pack()

        self.frame_table_outcome = customtkinter.CTkFrame(self.outcome_block)
        self.frame_table_outcome.pack(side="top")
            # Таблица 
        columns = ("1", "2", "3", "4")
        self.outcome_Table = ttk.Treeview(self.frame_table_outcome, show="headings", columns=columns, style="TableStyle.Treeview", height=18)
        self.outcome_Table.heading("1", text="#")
        self.outcome_Table.heading("2", text="Дата")
        self.outcome_Table.heading("3", text="Категория")
        self.outcome_Table.heading("4", text="Сумма")
        self.outcome_Table.column("2", width=84, anchor="center", minwidth=84, stretch=False)
        self.outcome_Table.column("3", minwidth=84, stretch=False)
        self.outcome_Table.column("4", anchor="center", minwidth=84, stretch=False)
        self.scrolltable_outcome = customtkinter.CTkScrollbar(self.frame_table_outcome, command=self.outcome_Table.yview)
        self.outcome_Table.configure(yscrollcommand=self.scrolltable_outcome.set)
        self.scrolltable_outcome.pack(side="right", fill="y")
        self.outcome_Table.pack(fill="both", expand=True)

        self.add_outcome = customtkinter.CTkButton(self.outcome_block, text="Добавить", command=self.show_input_window_outcome)
        self.add_outcome.pack(side="left")

        self.delete_outcome = customtkinter.CTkButton(self.outcome_block, text="Удалить", command=self.delete_record)
        self.delete_outcome.pack(side="right")

        # Долговой блок
        self.duty_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.duty_block, text="Долги")
        self.title_text.pack()

        self.frame_table_duty = customtkinter.CTkFrame(self.duty_block)
        self.frame_table_duty.pack(side="top")
            # Таблица 
        columns = ("1", "2", "3", "4", "5")
        self.duty_Table = ttk.Treeview(self.frame_table_duty, show="headings", columns=columns, style="TableStyle.Treeview", height=18)
        self.duty_Table.heading("1", text="#")
        self.duty_Table.heading("2", text="Заём")
        self.duty_Table.heading("3", text="Кому")
        self.duty_Table.heading("4", text="Возврат")
        self.duty_Table.heading("5", text="Сумма")
        self.duty_Table.column("2", width=87, anchor="center", minwidth=87, stretch=False)
        self.duty_Table.column("3", anchor="center", minwidth=87, stretch=False)
        self.duty_Table.column("4", width=87, anchor="center", minwidth=87, stretch=False)
        self.duty_Table.column("5", anchor="center", minwidth=87, stretch=False)
        self.scrolltable_duty = customtkinter.CTkScrollbar(self.frame_table_duty, command=self.duty_Table.yview)
        self.duty_Table.configure(yscrollcommand=self.scrolltable_duty.set)
        self.scrolltable_duty.pack(side="right", fill="y")
        self.duty_Table.pack(fill="both", expand=True)

        self.add_duty = customtkinter.CTkButton(self.duty_block, text="Добавить", command=self.show_input_window_duty)
        self.add_duty.pack(side="left")

        self.delete_duty = customtkinter.CTkButton(self.duty_block, text="Удалить", command=self.delete_record)
        self.delete_duty.pack(side="right")

        # Категории блок
        self.category_block = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.title_text = customtkinter.CTkLabel(self.category_block, text="Категории")
        self.title_text.pack()

        # Привязки для работы контроля размера таблиц
        self.income_Table.bind('<Button-1>', self.handle_click)
        self.outcome_Table.bind('<Button-1>', self.handle_click)
        self.duty_Table.bind('<Button-1>', self.handle_click)

    # Функция проверки поля с суммой
    def only_numbers(self, char):
        if char.isdigit() or char == ".":
            return True
        else:
            return False

    def handle_click(self, event):
        if self.income_Table.identify_region(event.x, event.y) == "separator":
            return "break"
        if self.outcome_Table.identify_region(event.x, event.y) == "separator":
            return "break"
        if self.duty_Table.identify_region(event.x, event.y) == "separator":
            return "break"
    
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
            self.reflesh_balance()
            self.main_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.duty_block.winfo_ismapped():
            self.duty_block.grid_forget()
            # self.reflesh_balance()
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
            self.refresh_tree_outcome()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.income_block.winfo_ismapped():
            self.income_block.grid_forget()
            self.refresh_tree_outcome()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.duty_block.winfo_ismapped():
            self.duty_block.grid_forget()
            self.refresh_tree_outcome()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.category_block.winfo_ismapped():
            self.category_block.grid_forget()
            self.refresh_tree_outcome()
            self.outcome_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

    def button_duty_block(self):
        if self.main_block.winfo_ismapped():
            self.main_block.grid_forget()
            self.refresh_tree_duty()
            self.duty_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.outcome_block.winfo_ismapped():
            self.outcome_block.grid_forget()
            self.refresh_tree_duty()
            self.duty_block.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=3)

        if self.income_block.winfo_ismapped():
            self.income_block.grid_forget()
            self.refresh_tree_duty()
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

    def save_input_income(self):
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

    def save_input_outcome(self):
        global entered_text
        self.first_entry = self.date_enter_outcome.get()
        self.two_entry = self.source_enter_outcome.get()
        self.three_entry = self.sum_enter_outcome.get()

        if not self.first_entry or not self.two_entry or not self.three_entry:
            messagebox.showerror("Ошибка", "Не все поля заполнены")
            self.input_window_outcome.focus_force()
            return

        self.enter_outcomebase = [self.first_entry, self.two_entry, self.three_entry]

        c.execute("INSERT INTO outcome_table (date, category, amount) VALUES (?, ?, ?)", (self.enter_outcomebase[0], self.enter_outcomebase[1], self.enter_outcomebase[2]))
        conn.commit()
        self.refresh_tree_outcome()
        self.input_window_outcome.destroy()

    def save_input_duty(self):
        global entered_text
        self.first_entry = self.date_enter_duty.get()
        self.two_entry = self.source_enter_duty.get()
        self.tw_three_entry = self.date_term_duty.get()
        self.three_entry = self.sum_enter_duty.get()

        if not self.first_entry or not self.two_entry or not self.three_entry or not self.tw_three_entry:
            messagebox.showerror("Ошибка", "Не все поля заполнены")
            self.input_window_duty.focus_force()
            return

        self.enter_dutybase = [self.first_entry, self.two_entry, self.three_entry, self.tw_three_entry]

        c.execute("INSERT INTO duty_table (date, people, description, amount) VALUES (?, ?, ?, ?)", (self.enter_dutybase[0], self.enter_dutybase[1], self.enter_dutybase[3],self.enter_dutybase[2]))
        conn.commit()
        self.refresh_tree_duty()
        self.input_window_duty.destroy()

    # Обновление таблицы доходов
    def refresh_tree_income(self):
        check_Exists = False
        self.income_Table.delete(*self.income_Table.get_children())
        c.execute("SELECT * FROM income_table")
        data_income = c.fetchall()
        print(data_income)
        data_income.reverse()
        for row in data_income:
            self.income_Table.insert("", "end", values=row)
        list_ID = []
        # list_SOURCE = []
        # list_MONEY = []
        c.execute("SELECT * FROM income_table")
        for i in c.fetchall():
            check_Exists = True
            list_ID.append(i[0])
            # list_SOURCE.append(i[2])
            # list_MONEY.append(i[3])
        if check_Exists:
            width_ID_column = max([self.my_font.measure(item) for item in list_ID])
            # width_SOURCE_column = max([self.my_font.measure(item) for item in list_SOURCE])
            # width_MONEY_column = max([self.my_font.measure(item) for item in list_MONEY])

            self.income_Table.column("1", width=width_ID_column+20)
        # self.income_Table.column("3", width=width_SOURCE_column+20)
        # self.income_Table.column("4", width=width_MONEY_column+50, anchor="center")

    # Обновление таблицы расходов
    def refresh_tree_outcome(self):
        check_Exists = False
        self.outcome_Table.delete(*self.outcome_Table.get_children())
        c.execute("SELECT * FROM outcome_table")
        data_outcome = c.fetchall()
        print(data_outcome)
        data_outcome.reverse()
        for row in data_outcome:
            self.outcome_Table.insert("", "end", values=row)
        list_ID = []
        list_SOURCE = []
        list_MONEY = []
        c.execute("SELECT * FROM outcome_table")
        for i in c.fetchall():
            check_Exists = True
            list_ID.append(i[0])
            list_SOURCE.append(i[2])
            list_MONEY.append(i[3])
        if check_Exists:
            width_ID_column = max([self.my_font.measure(item) for item in list_ID])
            width_SOURCE_column = max([self.my_font.measure(item) for item in list_SOURCE])
            width_MONEY_column = max([self.my_font.measure(item) for item in list_MONEY])

            self.outcome_Table.column("1", width=width_ID_column+20)
        # self.income_Table.column("3", width=width_SOURCE_column+20)
        # self.income_Table.column("4", width=width_MONEY_column+50, anchor="center")

    # Обновление таблицы долгов
    def refresh_tree_duty(self):
        check_Exists = False
        self.duty_Table.delete(*self.duty_Table.get_children())
        c.execute("SELECT * FROM duty_table")
        data_duty = c.fetchall()
        print(data_duty)
        data_duty.reverse()
        for row in data_duty:
            self.duty_Table.insert("", "end", values=row)
        list_ID = []
        list_SOURCE = []
        list_MONEY = []
        c.execute("SELECT * FROM duty_table")
        for i in c.fetchall():
            check_Exists = True
            list_ID.append(i[0])
            list_SOURCE.append(i[2])
            list_MONEY.append(i[3])
        if check_Exists:
            width_ID_column = max([self.my_font.measure(item) for item in list_ID])
            width_SOURCE_column = max([self.my_font.measure(item) for item in list_SOURCE])
            width_MONEY_column = max([self.my_font.measure(item) for item in list_MONEY])

            self.duty_Table.column("1", width=width_ID_column+20)
        # self.income_Table.column("3", width=width_SOURCE_column+20)
        # self.income_Table.column("4", width=width_MONEY_column+50, anchor="center")

    # Кнопка вызова окна для добавления новой записи дохода
    def show_input_window_income(self):
        self.input_window = customtkinter.CTkToplevel()
        self.input_window.title("Добавление записи")
        self.input_window.geometry(f"{300}x{200}")
        self.input_window.grab_set()

        # Сюда выбор даты вставлять
        self.data_text = customtkinter.CTkLabel(self.input_window, text="Дата:", width=100)
        self.data_text.grid(row=0, column=0, padx=10, pady=10)
        self.date_enter_income = DateEntry(self.input_window, width=20, background='blue', foreground="white", borderwidth=2, year=2023, locale="ru_RU")
        self.date_enter_income.grid(row=0, column=1, padx=10, pady=10)

        self.category_text = customtkinter.CTkLabel(self.input_window, text="Источник:", width=100)
        self.category_text.grid(row=1, column=0, padx=10, pady=10)
        self.source_enter_income = customtkinter.CTkEntry(self.input_window)
        self.source_enter_income.grid(row=1, column=1, padx=10, pady=10)

        # Сюда проверку на цифры сунуть
        self.money_count_text = customtkinter.CTkLabel(self.input_window, text="Сумма:", width=100)
        self.money_count_text.grid(row=2, column=0, padx=10, pady=10)
        self.sum_enter_income = customtkinter.CTkEntry(self.input_window)
        self.sum_enter_income.configure(validate="key", validatecommand=(self.register(self.only_numbers), "%S"))
        self.sum_enter_income.grid(row=2, column=1, padx=10, pady=10)

        self.submit_button = customtkinter.CTkButton(self.input_window, text="Подтвердить", command=self.save_input_income, width=50)
        self.submit_button.grid(row=3, column=0, padx=10, pady=10)

        self.dismit_button = customtkinter.CTkButton(self.input_window, text="Отмена", command=self.input_window.destroy, width=50)
        self.dismit_button.grid(row=3, column=1, padx=10, pady=10)

    # Кнопка вызова окна для добавления новой записи расхода
    def show_input_window_outcome(self):
        self.input_window_outcome = customtkinter.CTkToplevel()
        self.input_window_outcome.title("Добавление записи")
        self.input_window_outcome.geometry(f"{300}x{200}")
        self.input_window_outcome.grab_set()

        # Сюда выбор даты вставлять
        self.data_text = customtkinter.CTkLabel(self.input_window_outcome, text="Дата:", width=100)
        self.data_text.grid(row=0, column=0, padx=10, pady=10)
        self.date_enter_outcome = DateEntry(self.input_window_outcome, width=20, background='blue', foreground="white", borderwidth=2, year=2023, locale="ru_RU")
        self.date_enter_outcome.grid(row=0, column=1, padx=10, pady=10)

        self.category_text = customtkinter.CTkLabel(self.input_window_outcome, text="Категория:", width=100)
        self.category_text.grid(row=1, column=0, padx=10, pady=10)
        self.source_enter_outcome = customtkinter.CTkEntry(self.input_window_outcome)
        self.source_enter_outcome.grid(row=1, column=1, padx=10, pady=10)

        # Сюда проверку на цифры сунуть
        self.money_count_text = customtkinter.CTkLabel(self.input_window_outcome, text="Сумма:", width=100)
        self.money_count_text.grid(row=2, column=0, padx=10, pady=10)
        self.sum_enter_outcome = customtkinter.CTkEntry(self.input_window_outcome)
        self.sum_enter_outcome.configure(validate="key", validatecommand=(self.register(self.only_numbers), "%S"))
        self.sum_enter_outcome.grid(row=2, column=1, padx=10, pady=10)

        self.submit_button = customtkinter.CTkButton(self.input_window_outcome, text="Подтвердить", command=self.save_input_outcome, width=50)
        self.submit_button.grid(row=3, column=0, padx=10, pady=10)

        self.dismit_button = customtkinter.CTkButton(self.input_window_outcome, text="Отмена", command=self.input_window_outcome.destroy, width=50)
        self.dismit_button.grid(row=3, column=1, padx=10, pady=10)

    # Кнопка вызова окна для добавления новой записи долга
    def show_input_window_duty(self):
        self.input_window_duty = customtkinter.CTkToplevel()
        self.input_window_duty.title("Добавление долга")
        self.input_window_duty.geometry(f"{300}x{250}")
        self.input_window_duty.grab_set()

        # Сюда выбор даты вставлять
        self.data_text = customtkinter.CTkLabel(self.input_window_duty, text="Дата займа:", width=100)
        self.data_text.grid(row=0, column=0, padx=10, pady=10)
        self.date_enter_duty = DateEntry(self.input_window_duty, width=20, background='blue', foreground="white", borderwidth=2, year=2023, locale="ru_RU")
        self.date_enter_duty.grid(row=0, column=1, padx=10, pady=10)

        self.category_text = customtkinter.CTkLabel(self.input_window_duty, text="Кому должен:", width=100)
        self.category_text.grid(row=1, column=0, padx=10, pady=10)
        self.source_enter_duty = customtkinter.CTkEntry(self.input_window_duty)
        self.source_enter_duty.grid(row=1, column=1, padx=10, pady=10)

        self.data_text = customtkinter.CTkLabel(self.input_window_duty, text="Дата возврата:", width=100)
        self.data_text.grid(row=2, column=0, padx=10, pady=10)
        self.date_term_duty = DateEntry(self.input_window_duty, width=20, background='blue', foreground="white", borderwidth=2, year=2023, locale="ru_RU")
        self.date_term_duty.grid(row=2, column=1, padx=10, pady=10)

        # Сюда проверку на цифры сунуть
        self.money_count_text = customtkinter.CTkLabel(self.input_window_duty, text="Сумма:", width=100)
        self.money_count_text.grid(row=3, column=0, padx=10, pady=10)
        self.sum_enter_duty = customtkinter.CTkEntry(self.input_window_duty)
        self.sum_enter_duty.configure(validate="key", validatecommand=(self.register(self.only_numbers), "%S"))
        self.sum_enter_duty.grid(row=3, column=1, padx=10, pady=10)

        self.submit_button = customtkinter.CTkButton(self.input_window_duty, text="Подтвердить", command=self.save_input_duty, width=50)
        self.submit_button.grid(row=4, column=0, padx=10, pady=10)

        self.dismit_button = customtkinter.CTkButton(self.input_window_duty, text="Отмена", command=self.input_window_duty.destroy, width=50)
        self.dismit_button.grid(row=4, column=1, padx=10, pady=10)

    # Кнопка удаления записи в одной из трёх таблиц
    def delete_record(self):
        if self.income_block.winfo_ismapped():
            print(self.income_block.winfo_ismapped())
            selected_item = self.income_Table.focus()
            # item_id = self.income_Table.item(selected_item)["values"][0]
            item_id = self.income_Table.item(selected_item)["values"][0]
            self.income_Table.delete(selected_item)

            c.execute("DELETE FROM income_table WHERE id = ?", (item_id,))
            conn.commit()
        if self.outcome_block.winfo_ismapped():
            print(self.outcome_block.winfo_ismapped())
            selected_item = self.outcome_Table.focus()
            # item_id = self.income_Table.item(selected_item)["values"][0]
            item_id = self.outcome_Table.item(selected_item)["values"][0]
            self.outcome_Table.delete(selected_item)

            c.execute("DELETE FROM outcome_table WHERE id = ?", (item_id,))
            conn.commit()

        if self.duty_block.winfo_ismapped():
            print(self.duty_block.winfo_ismapped())
            selected_item = self.duty_Table.focus()
            # item_id = self.income_Table.item(selected_item)["values"][0]
            item_id = self.duty_Table.item(selected_item)["values"][0]
            self.duty_Table.delete(selected_item)

            c.execute("DELETE FROM duty_table WHERE id = ?", (item_id,))
            conn.commit()

    def reflesh_balance(self):
        c.execute("SELECT * FROM income_table")
        balance = 0
        for row in c.fetchall():
            balance += row[3]

        c.execute("SELECT * FROM outcome_table")
        for row in c.fetchall():
            balance = balance - row[3]
        print(balance)
        self.income_text.configure(text = "Баланс: "+str(balance))

if __name__ == "__main__":
    app = KrisMoney()
    app.mainloop()