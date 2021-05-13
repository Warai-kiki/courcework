import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_books = db_books
        self.db_daytime = db_daytime
        self.db_readers = db_readers
        self.view_timetable()
        self.view_catalog()

        self.root = root

    def init_main(self):
        toolbar = tk.Frame(bg='#EAC38D', bd=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # entering in the system
        self.add_img_2 = tk.PhotoImage(file='enter100.png')  # adding button pic
        btn_open_adding = tk.Button(toolbar, text='Вхід', command=self.open_login, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img_2)
        btn_open_adding.pack(side=tk.LEFT)
        # registration button
        self.img_reg = tk.PhotoImage(file='registration100.png')  # adding button pic
        btn_open_registr = tk.Button(toolbar, text='Реєстрація', command=self.open_registration, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.img_reg)
        btn_open_registr.pack(side=tk.LEFT)


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

    def open_registration(self):
        Registration()

    def open_login(self):
        Child_login()

    def open_search_dialog(self):
        SearchBooks()

    def open_search_dialog_auth(self):
        SearchAuthors()

# Авторизація
class Child_login(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_login()

    def btn_click(self):
        login = self.loginInput.get()
        password = self.passwordInput.get()

        if login == '' or password == '':
            info_str = f'Щось пішло не так. Спробуйте ще раз.'
            messagebox.showinfo(title='Помилка входу', message=info_str)
        else:
            info_str = f'Дані: {str(login)}, {str(password)}'
            messagebox.showinfo(title='Login', message=info_str)

        # вікно з помилкою
        # messagebox.showerror(title='', message='Error')

    def init_login(self):
        self.geometry('450x250+550+200')

        self.resizable(False, False)

        self.canvas = tk.Canvas(self, height=250, width=300)
        self.canvas.pack()

        self.frame = tk.Frame(self, bg='#79350B')
        self.frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)

        self.title = tk.Label(self.frame, text='Авторизація', bg='#C38661', font=40)
        self.title.pack()

        self.text_login = tk.Label(self.frame, text='Введіть email', bg='#C38661')
        self.text_login.pack(),
        self.loginInput = tk.Entry(self.frame, text='login', bg='#F9E7DD')
        self.loginInput.pack()
        self.text_pass = tk.Label(self.frame, text='Введіть пароль', bg='#C38661')
        self.text_pass.pack(),
        self.passwordInput = tk.Entry(self.frame, bg='#F9E7DD', show='@')
        self.passwordInput.pack()

        self.btn = tk.Button(self.frame, text='Вхід', bg='#79350B', command=self.btn_click)
        self.btn.pack()

        self.grab_set()
        self.focus_set()

# Реєстрація користувачів
class Registration(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.registration()

    def btn_click(self):
        name = self.entry_name.get()
        login = self.entry_email.get()
        password = self.entry_password.get()

        if login == '' or password == '' or name == '':
            info_str = f'Щось пішло не так. Спробуйте ще раз.'
            messagebox.showinfo(title='Помилка реєстрації', message=info_str)
        else:
            info_str = f'Ви успішно зареєстровані'
            messagebox.showinfo(title='Login', message=info_str)

    def registration(self):
        self.title('Реєстрація')
        self.geometry('450x250+550+200')
        self.resizable(False, False)

        file = open('readers.db', 'wb')

        self.canvas = tk.Canvas(self, height=250, width=300)
        self.canvas.pack()

        self.frame = tk.Frame(self, bg='#79350B')
        self.frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
        # назви полів вводу
        self.label_name = tk.Label(self.frame, text='ПІБ', bg='#C38661')
        self.label_name.place(x=70, y=40)
        self.label_email = tk.Label(self.frame, text='Email', bg='#C38661')
        self.label_email.place(x=60, y=70)
        self.label_password = tk.Label(self.frame, text='Пароль', bg='#C38661')
        self.label_password.place(x=50, y=100)

        self.entry_name = ttk.Entry(self.frame, text='name')
        self.entry_name.place(x=100, y=40)

        self.entry_email = ttk.Entry(self.frame, text='email')
        self.entry_email.place(x=100, y=70)

        self.entry_password = ttk.Entry(self.frame, show='@')
        self.entry_password.place(x=100, y=100)


        #self.btn_registr.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()


# Додати "замовлення"
class AddOrder(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add_order()
        self.view = app

    def init_add_order(self):
        self.title('Додати замовлення')
        self.geometry('550x450+550+200')
        self.resizable(False, False)

        # назви полів вводу
        label_name = tk.Label(self, text='ПІБ')
        label_name.place(x=50, y=50)
        label_book = tk.Label(self, text='Назва книги/журналу')
        label_book.place(x=50, y=80)
        label_user_id = tk.Label(self, text='ID користувача')
        label_user_id.place(x=50, y=110)
        label_took = tk.Label(self, text='Дата видачі/отримання\nзамовлення')
        label_took.place(x=50, y=140)
        label_return = tk.Label(self, text='Дата повернення')
        label_return.place(x=50, y=180)
        label_status = tk.Label(self, text='Статус')
        label_status.place(x=50, y=210)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_book = ttk.Entry(self)
        self.entry_book.place(x=200, y=80)

        self.entry_user_id = ttk.Entry(self)
        self.entry_user_id.place(x=200, y=110)

        self.entry_took = ttk.Entry(self)
        self.entry_took.place(x=200, y=145)

        self.entry_return = ttk.Entry(self)
        self.entry_return.place(x=200, y=180)

        self.combobox_status = ttk.Combobox(self, value=[u'Замовлено', u'Видано', u'Повернуто', u'Затримано'])
        self.combobox_status.current(0)
        self.combobox_status.place(x=200, y=210)

        self.btn_add = ttk.Button(self, text='Зберегти')
        self.btn_add.place(x=220, y=240)
        self.btn_add.bind('<Button-1>', lambda event: self.view.orders(self.entry_name.get(),
                                                                       self.entry_book.get(), self.entry_user_id.get(),
                                                                       self.entry_took.get(), self.entry_return.get(),
                                                                       self.combobox_status.get()))
        self.btn_add.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()

# Додати бібліотекаря до розкладу
class AddTimeLib(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_addlib()
        self.view = app

    def init_addlib(self):
        self.title('Редагувати розклад')
        self.geometry('550x450+550+200')
        self.resizable(False, False)

        # назви полів вводу
        label_name = tk.Label(self, text='Бібліотекар')
        label_name.place(x=50, y=50)
        label_mon = tk.Label(self, text='Понеділок')
        label_mon.place(x=50, y=80)
        label_tue = tk.Label(self, text='Вівторок')
        label_tue.place(x=50, y=110)
        label_wen = tk.Label(self, text='Середа')
        label_wen.place(x=50, y=140)
        label_thu = tk.Label(self, text='Четвер')
        label_thu.place(x=50, y=170)
        label_fri = tk.Label(self, text='Пятниця')
        label_fri.place(x=50, y=200)
        label_sut = tk.Label(self, text='Субота')
        label_sut.place(x=50, y=230)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.combobox_mon = ttk.Combobox(self, value=[u'09:00-14:00', u'14:00-19:00', u'-'])
        self.combobox_mon.current(0)
        self.combobox_mon.place(x=200, y=80)

        self.combobox_tue = ttk.Combobox(self, value=[u'09:00-14:00', u'14:00-19:00', u'-'])
        self.combobox_tue.current(0)
        self.combobox_tue.place(x=200, y=110)

        self.combobox_wen = ttk.Combobox(self, value=[u'09:00-14:00', u'14:00-19:00', u'-'])
        self.combobox_wen.current(0)
        self.combobox_wen.place(x=200, y=140)

        self.combobox_thu = ttk.Combobox(self, value=[u'09:00-14:00', u'14:00-19:00', u'-'])
        self.combobox_thu.current(0)
        self.combobox_thu.place(x=200, y=170)

        self.combobox_fri = ttk.Combobox(self, value=[u'09:00-14:00', u'14:00-19:00', u'-'])
        self.combobox_fri.current(0)
        self.combobox_fri.place(x=200, y=200)

        self.combobox_sut = ttk.Combobox(self, value=[u'10:00-14:00', u'14:00-18:00', u'-'])
        self.combobox_sut.current(0)
        self.combobox_sut.place(x=200, y=230)

        self.btn_add = ttk.Button(self, text='Зберегти')
        self.btn_add.place(x=220, y=260)
        self.btn_add.bind('<Button-1>', lambda event: self.view.timetable(self.entry_name.get(),
                                                                          self.combobox_mon.get(),
                                                                          self.combobox_tue.get(),
                                                                          self.combobox_wen.get(),
                                                                          self.combobox_thu.get(),
                                                                          self.combobox_fri.get(),
                                                                          self.combobox_sut.get()))
        self.btn_add.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()

# Додати дані бібілотекаря для входу в систему
class Add_Librarian(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Додати бібліотекаря')
        self.geometry('550x450+550+200')
        self.resizable(False, False)

        # назви полів вводу
        label_name = tk.Label(self, text='ПІБ')
        label_name.place(x=50, y=50)
        label_email = tk.Label(self, text='Email')
        label_email.place(x=50, y=80)
        label_password = tk.Label(self, text='Пароль')
        label_password.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_password = ttk.Entry(self)
        self.entry_password.place(x=200, y=110)

        self.btn_add = ttk.Button(self, text='Додати')
        self.btn_add.place(x=220, y=140)
        self.btn_add.bind('<Button-1>',
                          lambda event: self.view.librarians(self.entry_name.get(), self.entry_email.get(),
                                                             self.entry_password.get()))

        self.btn_add.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()

# Додати книгу до каталогу видань
class Add_book(tk.Toplevel):
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


#Редакція даних замовлень/формулярів
class UpdateOrderInfo(AddOrder):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db_orders = db_ordering
        self.default_data()

    def init_edit(self):
        self.title('Редагувати дані розкладу')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=220, y=260)
        btn_edit.bind('<Button>', lambda event: self.view.update_order(self.entry_name.get(),
                                                                       self.entry_book.get(), self.entry_user_id.get(),
                                                                       self.entry_took.get(), self.entry_return.get(),
                                                                       self.combobox_status.get()))
        self.btn_add.destroy()

    def default_data(self):
        self.db_orders.db_orders_conn.execute('''SELECT * FROM orders WHERE ID=?''',
                                               (self.view.tree_orders.set(self.view.tree_orders.selection()[0],'#1')))
        row = self.db_orders.db_orders_conn.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_book.insert(0, row[2])
        self.entry_user_id.insert(0, row[3])
        self.entry_took.insert(0, row[4])
        self.entry_return.insert(0, row[5])
        if row[6] != 'Замовлено':
            self.combobox_status.current(0)

#Редакція даних бібліотекарів
class UpdateTimeInfo(AddTimeLib):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db_daytime = db_daytime
        self.default_data()

    def init_edit(self):
        self.title('Редагувати дані розкладу')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=220, y=260)
        btn_edit.bind('<Button>', lambda event: self.view.update_timetable(self.entry_name.get(),
                                                                           self.combobox_mon.get(),
                                                                           self.combobox_tue.get(),
                                                                           self.combobox_wen.get(),
                                                                           self.combobox_thu.get(),
                                                                           self.combobox_fri.get(),
                                                                           self.combobox_sut.get()))
        self.btn_add.destroy() # нужно подумать как закрыть это окно при этом нормально отредактировав

# Редагувати дані робочого графіку бібліотекаря
class UpdateTimeLibrariansInfo(Add_Librarian):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db_readers = db_readers
        self.default_data()

    def init_edit(self):
        self.title('Редагувати дані\nчитача')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=220, y=200)
        btn_edit.bind('<Button>',
                      lambda event: self.view.update_readers_acc(self.entry_name.get(), self.entry_email.get(),
                                                                 self.entry_password.get()))
        self.btn_add.destroy()

    def default_data(self):
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers WHERE ID=?''',
                                                (self.view.tree_readers.set(self.view.tree_readers.selection()[0],
                                                                            '#1')))
        row = self.db_readers.db_readers_conn.fetchone()
        self.entry_name.insert(0, row[1])

    def default_data(self):
        self.db_daytime.db_timetable_conn.execute('''SELECT * FROM timetable WHERE ID=?''',
                                                  (self.view.tree_time.set(self.view.tree_time.selection()[0], '#1')))
        row = self.db_daytime.db_timetable_conn.fetchone()
        self.entry_name.insert(0,row[1])
        if row[2] != '09:00-14:00':
            if row[2] != '14:00-19:00':
                self.combobox_mon.current(2)
            else:
                self.combobox_mon.current(1)
        if row[3] != '09:00-14:00':
            if row[3] != '14:00-19:00':
                self.combobox_tue.current(2)
            else:
                self.combobox_tue.current(1)
        if row[4] != '09:00-14:00':
            if row[4] != '14:00-19:00':
                self.combobox_wen.current(2)
            else:
                self.combobox_wen.current(1)
        if row[5] != '09:00-14:00':
            if row[5] != '14:00-19:00':
                self.combobox_thu.current(2)
            else:
                self.combobox_thu.current(1)
        if row[6] != '09:00-14:00':
            if row[6] != '14:00-19:00':
                self.combobox_fri.current(2)
            else:
                self.combobox_fri.current(1)
        if row[7] != '10:00-14:00':
            if row[7] != '14:00-18:00':
                self.combobox_sut.current(2)
            else:
                self.combobox_sut.current(1)

#Редакція даних видань в каталозі
class UpdateBookInfo(Add_book):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db_books =db_books
        self.default_data()

    def init_edit(self):
        self.title('Редагувати дані книги')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=220, y=200)
        btn_edit.bind('<Button>', lambda event: self.view.update_catalog(self.entry_name.get(), self.entry_author.get(),
                                                                         self.combobox_type.get(),
                                                                         self.combobox_catagory.get(),
                                                                         self.combobox_hall.get()))
        self.btn_add.destroy() # нужно подумать как закрыть это окно при этом нормально отредактировав

    def default_data(self):
        self.db_books.db_books_conn.execute('''SELECT * FROM books WHERE ID=?''',
                                            (self.view.tree.set(self.view.tree.selection()[0],'#1')))
        row = self.db_books.db_books_conn.fetchone()
        self.entry_name.insert(0,row[1])
        if row[3] != 'Книга':
            self.combobox_type.current(1)

        self.entry_author.insert(0,row[2])
        self.num_box_cata = self.combobox_catagory.get()
        # нужно придумать как правильно вывести оставшиеся комбобоксы



# Пошук серед книг у каталозі
class SearchBooks(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

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

# Пошук у каталозі за автором
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

# Пошук формулярів за датою отримання (контроль видачі книг)
class SearchByDates(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук за датою')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_dates(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

#Пошук формулярів за статусом (відслідковування заборгованностей)
class SearchByStatus(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+600+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук\nзаборгованостей')
        label_search.place(x=10, y=20)

        self.search_status = ttk.Combobox(self, value=[u'Замовлено', u'Видано', u'Повернуто', u'Затримано'])
        self.search_status.current(0)
        self.search_status.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_orders_status(self.search_status.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Шукати розклад бібліотекаря за розкладом
class SearchLibrariansTime(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук бібліотекаря')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_librarians_time(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Пошук діних бібліотекаря
class SearchLibrarians(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук бібліотекаря')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_librarians_acc(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Пошук даних зареєстрованих читачів
class SearchReaders(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук читача')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_readers_acc(self.entry_search_2.get()))
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

# База даних зареєстрованих читачів
class DataBaseReaders:
    def __init__(self):
        self.db_readers = sqlite3.connect('readers.db')
        self.db_readers_conn = self.db_readers.cursor()
        self.db_readers_conn.execute('''CREATE TABLE IF NOT EXISTS readers (id integer primary key, name text, email text, password text)''')
        self.db_readers.commit()

    def insert_readers(self, name, email, password):
        self.db_readers_conn.execute('''INSERT INTO readers(name, email, password) VALUES (?, ?, ?)''',
                                     (name, email, password))

# База даних бібліотекарів
class DataBaseLibrarians:
    def __init__(self):
        self.db_librarians = sqlite3.connect('librarians.db')
        self.db_librarians_conn = self.db_librarians.cursor()
        self.db_librarians_conn.execute('''CREATE TABLE IF NOT EXISTS librarians (id integer primary key, name text, email text, password text)''')
        self.db_librarians.commit()

    def insert_librarians(self, name, email, password):
        self.db_librarians_conn.execute('''INSERT INTO librarians(name, email, password) VALUES (?, ?, ?)''',
                                        (name, email, password))

# база даних формулярів
class DataBaseOrders:
    def __init__(self):
        self.db_orders = sqlite3.connect('orders.db')
        self.db_orders_conn = self.db_orders.cursor()
        self.db_orders_conn.execute('''CREATE TABLE IF NOT EXISTS orders (id integer primary key, name text, book text, user_id integer, took text, need_return text, status text)''')
        self.db_orders.commit()

    def insert_order(self, name, book, user_id, took, need_return, status):
        self.db_orders_conn.execute('''INSERT INTO orders(name, book, user_id, took, need_return, status) VALUES (?, ?, ?, ?, ?, ?)''',
                                    (name, book, user_id, took, need_return, status))
        self.db_orders.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db_books = DataBaseBooks()
    db_daytime = DataBaseTimetable()
    db_readers = DataBaseReaders()
    db_librarians = DataBaseLibrarians()
    db_ordering = DataBaseOrders()
    app = Main(root)
    app.pack()
    root.title("Tiny Library")
    root.geometry("1250x700+180+70")
    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()
