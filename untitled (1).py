import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Глобальные переменные
expenses = []

# Загружаем данные из JSON
def load_data():
    global expenses
    try:
        with open('expenses.json', 'r') as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []

# Сохраняем данные в JSON
def save_data():
    with open('expenses.json', 'w') as f:
        json.dump(expenses, f, indent=4)

# Добавление расхода
def add_expense():
    amount_text = entry_amount.get()
    category = combo_category.get()
    date_text = entry_date.get()

    # Проверка корректности ввода
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Введите положительное число для суммы.")
        return

    # Проверка формата даты
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
        return

    expense = {
        "amount": amount,
        "category": category,
        "date": date_text
    }
    expenses.append(expense)
    save_data()
    refresh_treeview()
    clear_inputs()

# Очистка полей ввода
def clear_inputs():
    entry_amount.delete(0, tk.END)
    combo_category.set('')
    entry_date.delete(0, tk.END)

# Обновление таблицы
def refresh_treeview(filtered_expenses=None):
    for item in tree.get_children():
        tree.delete(item)
    data = filtered_expenses if filtered_expenses is not None else expenses
    for idx, exp in enumerate(data):
        tree.insert('', tk.END, iid=idx, values=(exp['amount'], exp['category'], exp['date']))

# Подсчёт суммы за выбранный период
def calculate_total():
    filtered = get_filtered_expenses()
    total = sum(exp['amount'] for exp in filtered)
    label_total.config(text=f"Общая сумма: {total:.2f}")

# Получение отфильтрованных расходов
def get_filtered_expenses():
    category_filter = combo_filter_category.get()
    date_filter = entry_filter_date.get()

    filtered = expenses
    if category_filter:
        filtered = [exp for exp in filtered if exp['category'] == category_filter]
    if date_filter:
        try:
            datetime.strptime(date_filter, "%Y-%m-%d")
            filtered = [exp for exp in filtered if exp['date'] == date_filter]
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату фильтра в формате ГГГГ-ММ-ДД.")
            return []
    return filtered

# Фильтр по категории
def apply_filter():
    filtered = get_filtered_expenses()
    refresh_treeview(filtered)
    calculate_total()

# Очистка фильтров
def clear_filter():
    combo_filter_category.set('')
    entry_filter_date.delete(0, tk.END)
    refresh_treeview()
    calculate_total()

# Инициализация GUI
load_data()
root = tk.Tk()
root.title("Expense Tracker")

# Ввод расхода
frame_input = ttk.Frame(root)
frame_input.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_input, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = ttk.Entry(frame_input)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Категория:").grid(row=0, column=2, padx=5, pady=5)
combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Другое"])
combo_category.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
entry_date = ttk.Entry(frame_input)
entry_date.grid(row=0, column=5, padx=5, pady=5)

btn_add = ttk.Button(frame_input, text="Добавить расход", command=add_expense)
btn_add.grid(row=0, column=6, padx=5, pady=5)

# Таблица расходов
columns = ('amount', 'category', 'date')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())

tree.pack(padx=10, pady=10, fill='both', expand=True)

# Фильтр
frame_filter = ttk.Frame(root)
frame_filter.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_filter, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
combo_filter_category = ttk.Combobox(frame_filter, values=["", "Еда", "Транспорт", "Развлечения", "Другое"])
combo_filter_category.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_filter, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
entry_filter_date = ttk.Entry(frame_filter)
entry_filter_date.grid(row=0, column=3, padx=5, pady=5)

btn_filter = ttk.Button(frame_filter, text="Применить фильтр", command=apply_filter)
btn_clear_filter = ttk.Button(frame_filter, text="Сбросить фильтр", command=clear_filter)
btn_filter.grid(row=0, column=4, padx=5, pady=5)
btn_clear_filter.grid(row=0, column=5, padx=5, pady=5)

# Область подсчёта
label_total = ttk.Label(root, text="Общая сумма: 0.00")
label_total.pack(pady=5)

# Инициализация таблицы
refresh_treeview()
calculate_total()

root.mainloop()