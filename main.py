import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Notebook
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_books = db_books
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



    def catalog(self, name, author, type, category, readinghall):
        self.db_books.insert_books(name, author, type, category, readinghall)
        self.view_catalog()

    def view_catalog(self):
        self.db_books.db_books_conn.execute('''SELECT * FROM books''')
        [self.tree.delete(i) for i in self.tree.get_children()] # отображение на экране
        [self.tree.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]

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


# Нове надходження
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Нове надходження')
        self.geometry('550x450+550+200')
        self.resizable(False, False)

        # назви полів вводу
        label_name = tk.Label(self, text='Назва')
        label_name.place(x=50, y=50)
        label_author = tk.Label(self, text='Автор')
        label_author.place(x=50, y=80)
        label_type = tk.Label(self, text='Тип')
        label_type.place(x=50, y=110)
        label_catagory = tk.Label(self, text='Категорія')
        label_catagory.place(x=50, y=140)
        label_hall = tk.Label(self, text='Читальний зал')
        label_hall.place(x=50, y=170)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_author = ttk.Entry(self)
        self.entry_author.place(x=200, y=80)

        self.combobox_type = ttk.Combobox(self, value=[u'Книга', u'Журнал'])
        self.combobox_type.current(0)
        self.combobox_type.place(x=200, y=110)

        self.combobox_catagory = ttk.Combobox(self, value=[u'Детективи', u'Дитяче', u'Іноземна класика', u'Історія',
                                                           u'Мода', u'Наукове', u'Психологія', u'Українська класика',
                                                           u'Фантастика', u'Фентезі', u'Філософія'])
        self.combobox_catagory.current(0)
        self.combobox_catagory.place(x=200, y=140)

        self.combobox_hall = ttk.Combobox(self, value=[u'№ 1', u'№ 2', u'№ 3', u'№ 4', u'№ 5'])
        self.combobox_hall.current(0)
        self.combobox_hall.place(x=200, y=170)

        '''btn_cancel = ttk.Button(self, text='Out'))
        btn_cancel.place(x=300, y=80)'''  # кнопка выхода

        self.btn_add = ttk.Button(self, text='Додати')
        self.btn_add.place(x=220, y=200)
        self.btn_add.bind('<Button-1>', lambda event: self.view.catalog(self.entry_name.get(), self.entry_author.get(),
                                                                         self.combobox_type.get(),
                                                                         self.combobox_catagory.get(),
                                                                         self.combobox_hall.get()))
        self.btn_add.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()

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
        self.geometry('450x250')

        self.resizable(False, False)

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

        self.btn = tk.Button(self.frame, text='Log in', bg='#79350B', command=self.btn_click)
        self.btn.pack()

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

if __name__ == "__main__":
    root = tk.Tk()
    db_books = DataBaseBooks()
    app = Main(root)
    app.pack()
    root.title("Tiny Library")
    root.geometry("1250x700+180+70")
    # root.protocol('WM_DELETE_WINDOW', window_deleted)
    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()
