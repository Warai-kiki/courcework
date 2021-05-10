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
        self.tab_1 = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_1, text='Каталог видань')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.tab_2 = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_2, text='Розклад роботи бібліотекарів')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        # table
        self.tree = ttk.Treeview(self.tab_1, column=('ID', 'name', 'author', 'type', 'category', 'reading_hall'), height=30,
                                 show='headings')

        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('author', width=250, anchor=tk.CENTER)
        self.tree.column('type', width=230, anchor=tk.CENTER)
        self.tree.column('category', width=250, anchor=tk.CENTER)
        self.tree.column('reading_hall', width=200, anchor=tk.CENTER)
        self.tree.column('ID', width=50, anchor=tk.CENTER)

        self.tree.heading('name', text='Назва')
        self.tree.heading('author', text='Автор')
        self.tree.heading('type', text='Тип')
        self.tree.heading('category', text='Категорія')
        self.tree.heading('reading_hall', text='Читальний зал')
        self.tree.heading('ID', text='ID')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # table
        self.tree_time = ttk.Treeview(self.tab_2, column=(
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
        [self.tree.delete(i) for i in self.tree.get_children()] # отображение на экране
        [self.tree.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]

    def timetable(self, name, monday, tuesday, wendsday, thursday, friday, saturday):
        self.db_daytime.insert_timetable(name, monday, tuesday, wendsday, thursday, friday, saturday)
        self.view_timetable()

    def view_timetable(self):
        self.db_daytime.db_timetable_conn.execute('''SELECT * FROM timetable''')
        [self.tree_time.delete(i) for i in self.tree_time.get_children()] # отображение на экране
        [self.tree_time.insert('', 'end', values=row) for row in self.db_daytime.db_timetable_conn.fetchall()]

    def search_in_catalog(self, name):
        name = ('%' + name + '%',)
        self.db_books.db_books_conn.execute('''SELECT * FROM books WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]

    def search_among_authors(self, author):
        author = ('%' + author + '%',)
        self.db_books.db_books_conn.execute('''SELECT * FROM books WHERE author LIKE ?''', author)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]


    def open_login(self):
        Child_login()

    def open_search_dialog(self):
        SearchBooks()

    def open_search_dialog_auth(self):
        SearchAuthors()

#
class Child_login(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_login()

    def btn_click(self):
        login = self.loginInput.get()
        password = self.passwordInput.get()

        if login == '' or password == '':
            info_str = f'Щось пішло не так. Спробуйте ще раз.'
            messagebox.showinfo(title='Login', message=info_str)
        else:
            info_str = f'Дані: {str(login)}, {str(password)}'
            messagebox.showinfo(title='Login', message=info_str)

        # вікно з помилкою
        # messagebox.showerror(title='', message='Error')

    def init_login(self):
        self.geometry('450x250+550+200')

        self.resizable(False, False)

        self.tabs_conrol = ttk.Notebook()
        self.tab_1 = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_1, text='Вхід')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self, height=250, width=300)
        self.canvas.pack()

        self.frame = tk.Frame(self, bg='#79350B')
        self.frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)

        self.title = tk.Label(self.frame, text='Авторизація', bg='#C38661', font=40)
        self.title.pack()

        self.loginInput = tk.Entry(self.frame, text='login', bg='#F9E7DD')
        self.loginInput.pack()
        self.passwordInput = tk.Entry(self.frame, bg='#F9E7DD', show='@')
        self.passwordInput.pack()

        self.btn = tk.Button(self.frame, text='Вхід', bg='#79350B', command=self.btn_click)
        self.btn.pack()

        self.btn_registration = tk.Button(self.frame, text='Реєстрація', bg='#79350B', command=self.btn_click)
        self.btn_registration.pack()

        self.grab_set()
        self.focus_set()


# Пошук серед книг
class SearchBooks(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        #self.title = tk.Label(self.frame, text='Пошук', bg='#C38661', font=40)
        #self.title.pack()

        label_search = tk.Label(self, text='Пошук видання')
        label_search.place(x=10, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_in_catalog(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class SearchAuthors(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        #self.title = tk.Label(self.frame, text='Пошук', bg='#C38661', font=40)
        #self.title.pack()

        label_search = tk.Label(self, text='Пошук автора')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_authors(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# база даних для книг
class DataBaseBooks:
    def __init__(self):
        self.db_books_c = sqlite3.connect('books.db')
        self.db_books_conn = self.db_books_c.cursor()
        self.db_books_conn.execute('''CREATE TABLE IF NOT EXISTS books  (id integer primary key, name text, author text, type text, category text, readinghall text)''')
        self.db_books_c.commit()

    def insert_books(self, name, author, type, category, readinghall):
        self.db_books_conn.execute('''INSERT INTO books(name, author, type, category, readinghall) VALUES (?, ?, ?, ?, ?)''',
                                   (name, author, type, category, readinghall))
        self.db_books_c.commit()

# база даних для розкладу
class DataBaseTimetable:
    def __init__(self):
        self.db_timetable = sqlite3.connect('timetable.db')
        self.db_timetable_conn = self.db_timetable.cursor()
        self.db_timetable_conn.execute('''CREATE TABLE IF NOT EXISTS timetable (id integer primary key, name text, monday text, tuesday text, wendsday text, thursday text, friday text, saturday text)''')
        self.db_timetable.commit()

    def insert_timetable(self, name, monday, tuesday, wendsday, thursday, friday, saturday):
        self.db_timetable_conn.execute('''INSERT INTO timetable(name, monday, tuesday, wendsday, thursday, friday, saturday) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                   (name, monday, tuesday, wendsday, thursday, friday, saturday))
        self.db_timetable.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db_books = DataBaseBooks()
    db_timetable = DataBaseTimetable()
    app = Main(root)
    app.pack()
    root.title("Tiny Library")
    root.geometry("1250x700+180+70")
    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()
