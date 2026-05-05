import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")

        # Инициализация переменных
        self.books = []

        # Создание GUI
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Автор").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Жанр").grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Количество страниц").grid(row=3, column=0)
        self.pages_entry = tk.Entry(self.root)
        self.pages_entry.grid(row=3, column=1)

        # Кнопка добавления книги
        self.add_button = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_button.grid(row=4, columnspan=2)

        # Фильтры
        tk.Label(self.root, text="Фильтровать по жанру").grid(row=5, column=0)
        self.genre_filter_entry = tk.Entry(self.root)
        self.genre_filter_entry.grid(row=5, column=1)

        self.filter_button = tk.Button(self.root, text="Фильтровать", command=self.filter_books)
        self.filter_button.grid(row=6, columnspan=2)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(self.root, columns=('title', 'author', 'genre', 'pages'), show='headings')
        for col in ('title', 'author', 'genre', 'pages'):
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=7, columnspan=2)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pages = self.pages_entry.get()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            pages = int(pages)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {'title': title, 'author': author, 'genre': genre, 'pages': pages}
        self.books.append(book)
        self.save_data()
        self.update_treeview()
        self.clear_entries()

    def filter_books(self):
        genre_filter = self.genre_filter_entry.get()
        filtered_books = [book for book in self.books if genre_filter.lower() in book['genre'].lower()]

        self.update_treeview(filtered_books)

    def update_treeview(self, books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if books is None:
            books = self.books

        for book in books:
            self.tree.insert('', 'end', values=(book['title'], book['author'], book['genre'], book['pages']))

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        self.genre_filter_entry.delete(0, tk.END)

    def save_data(self):
        with open('books.json', 'w') as f:
            json.dump(self.books, f)

    def load_data(self):
        if os.path.exists('books.json'):
            with open('books.json', 'r') as f:
                self.books = json.load(f)
                self.update_treeview()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
