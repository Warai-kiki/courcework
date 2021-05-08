import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_books = db_books
        self.db_daytime = db_timetable
        self.view_timetable()
        self.view_catalog()

        self.root = root

    def init_main(self):
        toolbar = tk.Frame(bg='#EAC38D', bd=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # entering in the system
        self.add_img_2 = tk.PhotoImage(file='enter-2.png')  # adding button pic
        btn_open_adding = tk.Button(toolbar, text='Вхід', command=self.open_login, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img_2)
        btn_open_adding.pack(side=tk.LEFT)


        # searching books
        self.search_img = tk.PhotoImage(file='search_80.png')
        btn_search = tk.Button(toolbar, text='Пошук видання', bg='#D19440', bd=1, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.RIGHT)
        # searching authors
        self.search_au_img = tk.PhotoImage(file='author_search_80.png')
        btn_search_auth = tk.Button(toolbar, text='Пошук автора', bg='#D19440', bd=1, image=self.search_au_img,
                               compound=tk.TOP, command=self.open_search_dialog_auth)
        btn_search_auth.pack(side=tk.RIGHT)
        # refreshing button
        self.refrech_img = tk.PhotoImage(file='refresh_80.png')
        btn_refresh = tk.Button(toolbar, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                    compound=tk.TOP, command=self.view_catalog)
        btn_refresh.pack(side=tk.RIGHT)

        self.tabs_conrol = ttk.Notebook()
        self.tab_1_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_1_lib, text='Каталог видань')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.tab_2_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_2_lib, text='Розклад роботи бібліотекарів')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        # table
        self.tree_libras = ttk.Treeview(self.tab_1_lib, column=('ID', 'name', 'author', 'type', 'category', 'reading_hall'), height=30,
                                        show='headings')

        self.tree_libras.column('name', width=250, anchor=tk.CENTER)
        self.tree_libras.column('author', width=250, anchor=tk.CENTER)
        self.tree_libras.column('type', width=230, anchor=tk.CENTER)
        self.tree_libras.column('category', width=250, anchor=tk.CENTER)
        self.tree_libras.column('reading_hall', width=200, anchor=tk.CENTER)
        self.tree_libras.column('ID', width=50, anchor=tk.CENTER)

        self.tree_libras.heading('name', text='Назва')
        self.tree_libras.heading('author', text='Автор')
        self.tree_libras.heading('type', text='Тип')
        self.tree_libras.heading('category', text='Категорія')
        self.tree_libras.heading('reading_hall', text='Читальний зал')
        self.tree_libras.heading('ID', text='ID')

        self.tree_libras.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree_libras.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree_libras.configure(yscrollcommand=scroll.set)

        # table
        self.tree_time = ttk.Treeview(self.tab_2_lib, column=(
        'ID', 'name', 'monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday'), height=30,
                                      show='headings')

        self.tree_time.column('ID', width=50, anchor=tk.CENTER)
        self.tree_time.column('name', width=260, anchor=tk.CENTER)
        self.tree_time.column('monday', width=150, anchor=tk.CENTER)
        self.tree_time.column('tuesday', width=150, anchor=tk.CENTER)
        self.tree_time.column('wendsday', width=150, anchor=tk.CENTER)
        self.tree_time.column('thursday', width=150, anchor=tk.CENTER)
        self.tree_time.column('friday', width=150, anchor=tk.CENTER)
        self.tree_time.column('saturday', width=150, anchor=tk.CENTER)

        self.tree_time.heading('ID', text='ID')
        self.tree_time.heading('name', text='Бібліотекар')
        self.tree_time.heading('monday', text='Понеділок')
        self.tree_time.heading('tuesday', text='Вівторок')
        self.tree_time.heading('wendsday', text='Середа')
        self.tree_time.heading('thursday', text='Черверг')
        self.tree_time.heading('friday', text='Пятниця')
        self.tree_time.heading('saturday', text='Субота')

        self.tree_time.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree_time.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree_time.configure(yscrollcommand=scroll.set)


    def catalog(self, name, author, type, category, readinghall):
        self.db_books.insert_books(name, author, type, category, readinghall)
        self.view_catalog()

    def view_catalog(self):
        self.db_books.db_books_conn.execute('''SELECT * FROM books''')
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()] # отображение на экране
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]

    def timetable(self, name, monday, tuesday, wendsday, thursday, friday, saturday):
        self.db_daytime.insert_timetable(name, monday, tuesday, wendsday, thursday, friday, saturday)
        self.view_timetable()

    def view_timetable(self):
        self.db_daytime.db_librarians_conn.execute('''SELECT * FROM timetable''')
        [self.tree_time.delete(i) for i in self.tree_time.get_children()] # отображение на экране
        [self.tree_time.insert('', 'end', values=row) for row in self.db_daytime.db_librarians_conn.fetchall()]

    def search_in_catalog(self, name):
        name = ('%' + name + '%',)
        self.db_books.db_books_conn.execute('''SELECT * FROM books WHERE name LIKE ?''', name)
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()]
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]

    def search_among_authors(self, author):
        author = ('%' + author + '%',)
        self.db_books.db_books_conn.execute('''SELECT * FROM books WHERE author LIKE ?''', author)
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()]
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]


    def open_login(self):
        Child_login()

    def open_search_dialog(self):
        SearchBooks()

# база даних для розкладу
class DataBaseLibrarians:
    def __init__(self):
        self.db_librarians = sqlite3.connect('librarians.db')
        self.db_librarians_conn = self.db_librarians.cursor()
        self.db_librarians_conn.execute('''CREATE TABLE IF NOT EXISTS librarians (id integer primary key, name text, surname text, phone text, email text)''')
        self.db_librarians.commit()

    def insert_timetable(self, name, surname, phone, email):
        self.db_librarians_conn.execute('''INSERT INTO librarians(id, name, surname, phone, email) VALUES (?, ?, ?, ?, ?)''',
                                        (name, surname, phone, email))