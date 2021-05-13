import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_books = db_books
        self.db_readers = db_readers
        self.db_librarians = db_librarians
        self.db_daytime = db_daytime
        self.db_order = db_ordering

        self.view_orders()
        self.view_timetable()
        self.view_librarians_acc()
        self.view_readers_acc()
        self.view_catalog()

        self.root = root

    def init_main(self):
        toolbar = tk.Frame(bg='#EAC38D', bd=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.tabs_conrol = ttk.Notebook()
        self.tab_1_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_1_lib, text='Бібліотекарі')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.tab_2_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_2_lib, text='Читачі')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.tab_3_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_3_lib, text='Каталог видань')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.tab_4_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_4_lib, text='Розклад роботи')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        self.tab_5_lib = tk.Frame(self.tabs_conrol)
        self.tabs_conrol.add(self.tab_5_lib, text='Контроль видач')
        self.tabs_conrol.pack(fill=tk.BOTH, expand=1)

        # out of the account
        self.add_img_2 = tk.PhotoImage(file='sign_out.png')  # adding button pic
        btn_open_adding = tk.Button(self.tab_1_lib, text='Вихід', command=self.sign_out, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img_2)
        btn_open_adding.place(x=1140, y=460)

        # adding button for librarians
        self.add_img = tk.PhotoImage(file='icons8-160.png')  # adding button pic
        btn_open_adding = tk.Button(self.tab_1_lib, text='Додати\nбібліотекаря', command=self.open_adding_libs,
                                    bg='#D19440', bd=1, compound=tk.TOP, image=self.add_img)
        btn_open_adding.place(x=0, y=4)
        # update button for librarians
        self.update_img = tk.PhotoImage(file='edit_160_2.png')
        btn_edit_dialog = tk.Button(self.tab_1_lib, text='Редагувати\nбібліотекаря', bg='#D19440', bd=1,
                                    image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_librs)
        btn_edit_dialog.place(x=0, y=204)
        # delete button for librarians
        self.delete_img = tk.PhotoImage(file='delete_160.png')
        btn_delete = tk.Button(self.tab_1_lib, text='Видалити\nбібліотекаря', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_librarian_acc)
        btn_delete.place(x=0, y=404)
        # searching for librarians
        self.search_people = tk.PhotoImage(file='author_search_80.png')
        btn_search = tk.Button(self.tab_1_lib, text='Пошук\nбібліотекаря', bg='#D19440', bd=1, image=self.search_people,
                               compound=tk.TOP, command=self.open_search_libr)
        btn_search.place(x=1160, y=4)
        # refreshing button for librarians
        self.refrech_img = tk.PhotoImage(file='refresh_80.png')
        btn_refresh_lib = tk.Button(self.tab_1_lib, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                    compound=tk.TOP, command=self.view_librarians_acc)
        btn_refresh_lib.place(x=1160, y=130)

        # update button for readers
        btn_edit_dialog_read = tk.Button(self.tab_2_lib, text='Редагувати\nчитача', bg='#D19440', bd=1,
                                         image=self.update_img,
                                         compound=tk.TOP, command=self.open_update_readers)
        btn_edit_dialog_read.place(x=0, y=4)
        # delete button for readers
        btn_delete_reader = tk.Button(self.tab_2_lib, text='Видалити\nчитача', bg='#D19440', bd=1,
                                      image=self.delete_img,
                                      compound=tk.TOP, command=self.delete_readers_acc)
        btn_delete_reader.place(x=0, y=204)
        # searching for readers
        btn_search_reader = tk.Button(self.tab_2_lib, text='Пошук читача', bg='#D19440', bd=1, image=self.search_people,
                                      compound=tk.TOP, command=self.open_search_read)
        btn_search_reader.place(x=1160, y=4)
        # refreshing button for readers
        btn_refresh = tk.Button(self.tab_2_lib, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                compound=tk.TOP, command=self.view_readers_acc)
        btn_refresh.place(x=1160, y=130)

        # adding book button pic
        btn_open_adding = tk.Button(self.tab_3_lib, text='Додати книгу', command=self.open_adding, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_adding.place(x=0, y=4)
        # update button
        btn_edit_dialog = tk.Button(self.tab_3_lib, text='Редагувати', bg='#D19440', bd=1, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.place(x=0, y=194)
        # delete button
        btn_delete = tk.Button(self.tab_3_lib, text='Видалити', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_books)
        btn_delete.place(x=0, y=384)
        # searching books
        self.search_img = tk.PhotoImage(file='search_80.png')
        btn_search = tk.Button(self.tab_3_lib, text='Пошук видання', bg='#D19440', bd=1, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.place(x=1150, y=4)
        # searching authors
        btn_search_auth = tk.Button(self.tab_3_lib, text='Пошук автора', bg='#D19440', bd=1, image=self.search_people,
                               compound=tk.TOP, command=self.open_search_dialog_auth)
        btn_search_auth.place(x=1150, y=110)
        # refreshing button
        btn_refresh = tk.Button(self.tab_3_lib, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                    compound=tk.TOP, command=self.view_catalog)
        btn_refresh.place(x=1150, y=220)

        # adding book to timetable
        btn_open_adding = tk.Button(self.tab_4_lib, text='Додати бібліотекаря', command=self.open_add_libro, bg='#D19440',
                                    bd=1, compound=tk.TOP, image=self.add_img)
        btn_open_adding.place(x=0, y=4)
        # update button to timetable
        btn_edit_dialog = tk.Button(self.tab_4_lib, text='Редагувати', bg='#D19440', bd=1, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog_libr)
        btn_edit_dialog.place(x=0, y=194)
        # delete button to timetable
        btn_delete = tk.Button(self.tab_4_lib, text='Видалити', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_libros_time)
        btn_delete.place(x=0, y=384)

        # searching librarian to timetable
        btn_search_auth = tk.Button(self.tab_4_lib, text='Пошук\nбібліотекаря', bg='#D19440', bd=1, image=self.search_people,
                                    compound=tk.TOP, command=self.open_search_dialog_libr)
        btn_search_auth.place(x=1150, y=4)
        # refreshing button to timetable
        btn_refresh = tk.Button(self.tab_4_lib, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                compound=tk.TOP, command=self.view_timetable)
        btn_refresh.place(x=1150, y=130)

        # adding book for order
        btn_open_adding = tk.Button(self.tab_5_lib, text='Додати книгу', command=self.open_add_order, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_adding.place(x=0, y=4)
        # update button for order
        btn_edit_dialog = tk.Button(self.tab_5_lib, text='Редагувати', bg='#D19440', bd=1, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog_order)
        btn_edit_dialog.place(x=0, y=194)
        # delete button for order
        btn_delete = tk.Button(self.tab_5_lib, text='Видалити', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_order)
        btn_delete.place(x=0, y=384)
        # searching for order
        self.search_stat_img = tk.PhotoImage(file='search_80.png')
        btn_search_stat = tk.Button(self.tab_5_lib, text='Пошук\nзаборгованостей', bg='#D19440', bd=1,
                                    image=self.search_stat_img,
                                    compound=tk.TOP, command=self.open_search_by_status)
        btn_search_stat.place(x=1150, y=4)
        # searching readers for order
        btn_search_date = tk.Button(self.tab_5_lib, text='Пошук\nчитача', bg='#D19440', bd=1, image=self.search_people,
                                    compound=tk.TOP, command=self.open_search_dialog_order)
        btn_search_date.place(x=1150, y=130)
        # searching for order
        self.search_date_img = tk.PhotoImage(file='icons8-поиск-в-списке-80.png')
        btn_search_date = tk.Button(self.tab_5_lib, text='Пошук по даті\nвидачі', bg='#D19440', bd=1,
                                    image=self.search_date_img,
                                    compound=tk.TOP, command=self.open_search_by_dates)
        btn_search_date.place(x=1150, y=256)
        # refreshing button for order
        btn_refresh = tk.Button(self.tab_5_lib, text='Оновити\n', bg='#D19440', bd=1, image=self.refrech_img,
                                compound=tk.TOP, command=self.view_orders)
        btn_refresh.place(x=1150, y=382)


        # table
        self.tree = ttk.Treeview(self.tab_3_lib, column=('ID', 'name', 'author', 'type', 'category', 'reading_hall'), height=30,
                                 show='headings')

        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('author', width=250, anchor=tk.CENTER)
        self.tree.column('type', width=100, anchor=tk.CENTER)
        self.tree.column('category', width=200, anchor=tk.CENTER)
        self.tree.column('reading_hall', width=100, anchor=tk.CENTER)
        self.tree.column('ID', width=50, anchor=tk.CENTER)

        self.tree.heading('name', text='Назва')
        self.tree.heading('author', text='Автор')
        self.tree.heading('type', text='Тип')
        self.tree.heading('category', text='Категорія')
        self.tree.heading('reading_hall', text='Читальний зал')
        self.tree.heading('ID', text='ID')

        self.tree.place(x=170, y=4, height=670)

        scroll = tk.Scrollbar(self.tab_3_lib, command=self.tree.yview)
        scroll.place(x=1120, y=4, height=670)
        self.tree.configure(yscrollcommand=scroll.set)

        # table  for librarians
        self.tree_libras = ttk.Treeview(self.tab_1_lib, column=('ID', 'name', 'email'), height=30,
                                        show='headings')

        self.tree_libras.column('ID', width=50, anchor=tk.CENTER)
        self.tree_libras.column('name', width=500, anchor=tk.CENTER)
        self.tree_libras.column('email', width=400, anchor=tk.CENTER)

        self.tree_libras.heading('ID', text='ID')
        self.tree_libras.heading('name', text='ПІБ')
        self.tree_libras.heading('email', text='Email')

        self.tree_libras.place(x=170, y=4, height=670)

        scroll = tk.Scrollbar(self.tab_1_lib, command=self.tree_libras.yview)
        scroll.place(x=1120, y=4, height=670)
        self.tree_libras.configure(yscrollcommand=scroll.set)

        # table for readers
        self.tree_readers = ttk.Treeview(self.tab_2_lib,
                                         column=('ID', 'name', 'email'), height=30,
                                         show='headings')

        self.tree_readers.column('ID', width=50, anchor=tk.CENTER)
        self.tree_readers.column('name', width=500, anchor=tk.CENTER)
        self.tree_readers.column('email', width=400, anchor=tk.CENTER)

        self.tree_readers.heading('ID', text='ID')
        self.tree_readers.heading('name', text='Назва')
        self.tree_readers.heading('email', text='Email')

        self.tree_readers.place(x=170, y=4, height=670)

        scroll = tk.Scrollbar(self.tab_2_lib, command=self.tree_readers.yview)
        scroll.place(x=1120, y=4, height=670)
        self.tree_readers.configure(yscrollcommand=scroll.set)

        # table to timetable
        self.tree_time = ttk.Treeview(self.tab_4_lib, column=(
        'ID', 'name', 'monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday'), height=30, show='headings')

        self.tree_time.column('ID', width=50, anchor=tk.CENTER)
        self.tree_time.column('name', width=260, anchor=tk.CENTER)
        self.tree_time.column('monday', width=100, anchor=tk.CENTER)
        self.tree_time.column('tuesday', width=100, anchor=tk.CENTER)
        self.tree_time.column('wendsday', width=100, anchor=tk.CENTER)
        self.tree_time.column('thursday', width=100, anchor=tk.CENTER)
        self.tree_time.column('friday', width=100, anchor=tk.CENTER)
        self.tree_time.column('saturday', width=100, anchor=tk.CENTER)

        self.tree_time.heading('ID', text='ID')
        self.tree_time.heading('name', text='Бібліотекар')
        self.tree_time.heading('monday', text='Понеділок')
        self.tree_time.heading('tuesday', text='Вівторок')
        self.tree_time.heading('wendsday', text='Середа')
        self.tree_time.heading('thursday', text='Черверг')
        self.tree_time.heading('friday', text='Пятниця')
        self.tree_time.heading('saturday', text='Субота')

        self.tree_time.place(x=170, y=4, height=670)

        scroll = tk.Scrollbar(self.tab_4_lib, command=self.tree_time.yview)
        scroll.place(x=1080, y=4, height=670)
        self.tree_time.configure(yscrollcommand=scroll.set)

        # table for order
        self.tree_orders = ttk.Treeview(self.tab_5_lib, column=('ID', 'name', 'book', 'user_id', 'took', 'need_return', 'status'),
                                 height=30,
                                 show='headings')

        self.tree_orders.column('ID', width=50, anchor=tk.CENTER)
        self.tree_orders.column('name', width=250, anchor=tk.CENTER)
        self.tree_orders.column('book', width=250, anchor=tk.CENTER)
        self.tree_orders.column('user_id', width=100, anchor=tk.CENTER)
        self.tree_orders.column('took', width=100, anchor=tk.CENTER)
        self.tree_orders.column('need_return', width=100, anchor=tk.CENTER)
        self.tree_orders.column('status', width=100, anchor=tk.CENTER)

        self.tree_orders.heading('ID', text='ID')
        self.tree_orders.heading('name', text='Читач')
        self.tree_orders.heading('book', text='Книга/Журнал')
        self.tree_orders.heading('user_id', text='ID користувача')
        self.tree_orders.heading('took', text='Дата видачі')
        self.tree_orders.heading('need_return', text='Дата повернення')
        self.tree_orders.heading('status', text='Статус')

        self.tree_orders.place(x=170, y=4, height=670)

        scroll = tk.Scrollbar(self, command=self.tree_orders.yview)
        scroll.place(x=1160, y=4, height=670)
        self.tree_orders.configure(yscrollcommand=scroll.set)


    def catalog(self, name, author, type, category, readinghall):
        self.db_books.insert_books(name, author, type, category, readinghall)
        self.view_catalog()

    def update_catalog(self, name, author, type, category, readinghall):
        self.db_books.db_books_c.execute('''UPDATE books SET name=?, author=?, type=?, category=?, readinghall=? WHERE ID=?''',
                                         (name, author, type, category, readinghall, self.tree.set(self.tree.selection()[0], '#1')))
        self.db_books.db_books_c.commit()
        self.view_catalog()

    def view_catalog(self):
        self.db_books.db_books_conn.execute('''SELECT * FROM books''')
        [self.tree.delete(i) for i in self.tree.get_children()] # отображение на экране
        [self.tree.insert('', 'end', values=row) for row in self.db_books.db_books_conn.fetchall()]

    def delete_books(self):
        for selection_item in self.tree.selection():
            self.db_books.db_books_c.execute('''DELETE FROM books WHERE ID=?''', (self.tree.set(selection_item, '#1')))
        self.db_books.db_books_c.commit()
        self.view_catalog()

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

    def readers_acc(self, name, email, password):
        self.db_readers.insert_readers(name, email, password)
        self.view_readers_acc()

    def view_readers_acc(self):
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers''')
        [self.tree_readers.delete(i) for i in self.tree_readers.get_children()]  # отображение на экране
        [self.tree_readers.insert('', 'end', values=row) for row in self.db_readers.db_readers_conn.fetchall()]

    def librarians_acc(self, name, email, password):
        self.db_librarians.insert_librarians(name, email, password)
        self.view_librarians_acc()

    def view_librarians_acc(self):
        self.db_librarians.db_librarians_conn.execute('''SELECT * FROM librarians''')
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()]  # отображение на экране
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_librarians.db_librarians_conn.fetchall()]

    def update_librarian_acc(self, name, email, password):
        self.db_librarians.db_librarians_conn.execute('''UPDATE librarians SET name=?, email=?, password=?''',
                                                      (name, email, password,
                                                       self.tree_libras.set(self.tree_libras.selection()[0], '#1')))
        self.db_librarians.db_librarians_conn.commit()
        self.view_librarians_acc()

    def delete_librarian_acc(self):
        for selection_item in self.tree_libras.selection():
            self.db_librarians.db_librarians_conn.execute('''DELETE FROM librarians WHERE ID=?''',
                                                          (self.tree_libras.set(selection_item, '#1')))
        self.db_librarians.db_librarians_conn.commit()
        self.view_librarians_acc()

    def update_readers_acc(self, name, email, password):
        self.db_readers.db_readers_conn.execute('''UPDATE readers SET name=?, email=?, password=?''',
                                                (name, email, password,
                                                 self.tree_readers.set(self.tree_readers.selection()[0], '#1')))
        self.db_readers.db_readers_conn.commit()
        self.view_readers_acc()

    def delete_readers_acc(self):
        for selection_item in self.tree_readers.selection():
            self.db_readers.db_readers_conn.execute('''DELETE FROM readers WHERE ID=?''',
                                                    (self.tree_readers.set(selection_item, '#1')))
        self.db_readers.db_readers_conn.commit()
        self.view_readers_acc()

    def search_among_librarians_acc(self, name):
        name = ('%' + name + '%',)
        self.db_librarians.db_librarians_conn.execute('''SELECT * FROM librarians WHERE name LIKE ?''', name)
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()]
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_librarians.db_librarians_conn.fetchall()]

    def search_among_readers_acc(self, name):
        name = ('%' + name + '%',)
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers WHERE name LIKE ?''', name)
        [self.tree_readers.delete(i) for i in self.tree_readers.get_children()]
        [self.tree_readers.insert('', 'end', values=row) for row in self.db_readers.db_readers_conn.fetchall()]

    def timetable(self, name, monday, tuesday, wendsday, thursday, friday, saturday):
        self.db_daytime.insert_timetable(name, monday, tuesday, wendsday, thursday, friday, saturday)
        self.view_timetable()

    def view_timetable(self):
        self.db_daytime.db_timetable_conn.execute('''SELECT * FROM timetable''')
        [self.tree_time.delete(i) for i in self.tree_time.get_children()] # отображение на экране
        [self.tree_time.insert('', 'end', values=row) for row in self.db_daytime.db_timetable_conn.fetchall()]

    def update_timetable(self, name, monday, tuesday, wendsday, thursday, friday, saturday):
        self.db_daytime.db_timetable.execute('''UPDATE timetable SET name=?, monday=?, tuesday=?, wendsday=?, thursday=?, friday=?, saturday=? WHERE ID=?''',
                                             (name, monday, tuesday, wendsday, thursday, friday, saturday, self.tree_time.set(self.tree_time.selection()[0], '#1')))
        self.db_daytime.db_timetable.commit()
        self.view_timetable()

    def delete_libros_time(self):
        for selection_item in self.tree_time.selection():
            self.db_daytime.db_timetable.execute('''DELETE FROM timetable WHERE ID=?''', (self.tree_time.set(selection_item, '#1')))
        self.db_daytime.db_timetable.commit()
        self.view_timetable()

    def search_among_librarians_time(self, author):
        author = ('%' + author + '%',)
        self.db_daytime.db_timetable_conn.execute('''SELECT * FROM timetable WHERE author LIKE ?''', author)
        [self.tree_time.delete(i) for i in self.tree_time.get_children()]
        [self.tree_time.insert('', 'end', values=row) for row in self.db_daytime.db_timetable_conn.fetchall()]

    def orders(self, name, book, user_id, took, need_return, status):
        self.db_order.insert_order(name, book, user_id, took, need_return, status)
        self.view_orders()

    def view_orders(self):
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders''')
        [self.tree_orders.delete(i) for i in self.tree_orders.get_children()] # отображение на экране
        [self.tree_orders.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def update_order(self, name, book, user_id, took, need_return, status):
        self.db_order.db_orders.execute('''UPDATE orders SET name=?, book=?, user_id=?, took=?, need_return=?, status=? WHERE ID=?''',
                                        (name, book, user_id, took, need_return, status, self.tree_orders.set(self.tree_orders.selection()[0], '#1')))
        self.db_order.db_orders.commit()
        self.view_orders()

    def delete_order(self):
        for selection_item in self.tree_orders.selection():
            self.db_order.db_orders.execute('''DELETE FROM orders WHERE ID=?''', (self.tree_orders.set(selection_item, '#1')))
        self.db_order.db_orders.commit()
        self.view_orders()

    def search_in_ord_catalog(self, name):
        name = ('%' + name + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE name LIKE ?''', name)
        [self.tree_orders.delete(i) for i in self.tree_orders.get_children()]
        [self.tree_orders.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def search_among_orders_status(self, status):
        status = ('%' + status + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE author LIKE ?''', status)
        [self.tree_orders.delete(i) for i in self.tree_orders.get_children()]
        [self.tree_orders.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def search_among_dates(self, date):
        date = ('%' + date + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE took LIKE ?''', date)
        [self.tree_orders.delete(i) for i in self.tree_orders.get_children()]
        [self.tree_orders.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def search_among_need_to_back(self, date):
        date = ('%' + date + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE need_return LIKE ?''', date)
        [self.tree_orders.delete(i) for i in self.tree_orders.get_children()]
        [self.tree_orders.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def open_add_order(self):
        AddOrder()

    def open_update_dialog_order(self):
        UpdateOrderInfo()

    def open_search_dialog_order(self):
        SearchOrder()

    def open_search_by_status(self):
        SearchByStatus()

    def open_search_by_dates(self):
        SearchDates()

    def open_add_libro(self):
        AddTimeLib()

    def open_update_dialog_libr(self):
        UpdateTimeInfo()

    def open_search_dialog_libr(self):
        SearchLibrariansTime()

    def open_adding_libs(self):
        Add_Librarian()

    def open_update_librs(self):
        UpdateLibrariansInfo()

    def open_update_readers(self):
        UpdateReadersInfo()

    def open_search_libr(self):
        SearchLibrarians()

    def open_search_read(self):
        SearchReaders()

    def open_adding(self):
        Add_book()

    def sign_out(self):
        Sign_out()

    def open_update_dialog(self):
        UpdateBookInfo()

    def open_search_dialog(self):
        SearchBooks()

    def open_search_dialog_auth(self):
        SearchAuthors()


# Нове надходження
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

#
class Sign_out(tk.Toplevel):
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

#Редакція даних
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

# Пошук серед книг
class SearchBooks(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук автора')
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

        label_search = tk.Label(self, text='Пошук видання')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_authors(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class SearchLibrarians(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук видання')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_librarians_acc(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class SearchReaders(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Пошук видання')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_readers_acc(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


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


class UpdateLibrariansInfo(Add_Librarian):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db_librarians =db_librarians
        self.default_data()

    def init_edit(self):
        self.title('Редагувати дані\nбібліотекаря')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=220, y=200)
        btn_edit.bind('<Button>', lambda event: self.view.update_librarian_acc(self.entry_name.get(), self.entry_email.get(),
                                                                               self.entry_password.get()))
        self.btn_add.destroy() # нужно подумать как закрыть это окно при этом нормально отредактировав

    def default_data(self):
        self.db_librarians.db_librarians_conn.execute('''SELECT * FROM librarians WHERE ID=?''',
                                                 (self.view.tree_libras.set(self.view.tree_libras.selection()[0],'#1')))
        row = self.db_librarians.db_librarians_conn.fetchone()
        self.entry_name.insert(0,row[1])

class UpdateReadersInfo(Add_Librarian):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db_readers =db_readers
        self.default_data()

    def init_edit(self):
        self.title('Редагувати дані\nчитача')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=220, y=200)
        btn_edit.bind('<Button>', lambda event: self.view.update_readers_acc(self.entry_name.get(), self.entry_email.get(),
                                                                             self.entry_password.get()))
        self.btn_add.destroy()

    def default_data(self):
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers WHERE ID=?''',
                                                 (self.view.tree_readers.set(self.view.tree_readers.selection()[0],'#1')))
        row = self.db_readers.db_readers_conn.fetchone()
        self.entry_name.insert(0,row[1])

# Додати бібліотекаря
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

#Редакція даних
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

#
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

#Редакція даних
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

# Пошук
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
#
class SearchOrder(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        #self.title = tk.Label(self.frame, text='Пошук', bg='#C38661', font=40)
        #self.title.pack()

        label_search = tk.Label(self, text='Пошук замовлення')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_in_ord_catalog(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class SearchDates(tk.Toplevel):
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

# база даних
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

# база даних
class DataBaseLibrarians:
    def __init__(self):
        self.db_librarians = sqlite3.connect('librarians.db')
        self.db_librarians_conn = self.db_librarians.cursor()
        self.db_librarians_conn.execute('''CREATE TABLE IF NOT EXISTS librarians (id integer primary key, name text, email text, password text)''')
        self.db_librarians.commit()

    def insert_librarians(self, name, email, password):
        self.db_librarians_conn.execute('''INSERT INTO librarians(name, email, password) VALUES (?, ?, ?)''',
                                        (name, email, password))

class DataBaseReaders:
    def __init__(self):
        self.db_readers = sqlite3.connect('readers.db')
        self.db_readers_conn = self.db_readers.cursor()
        self.db_readers_conn.execute('''CREATE TABLE IF NOT EXISTS readers (id integer primary key, name text, email text, password text)''')
        self.db_readers.commit()

    def insert_readers(self, name, email, password):
        self.db_readers_conn.execute('''INSERT INTO readers(name, email, password) VALUES (?, ?, ?)''',
                                     (name, email, password))

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
    db_readers = DataBaseReaders()
    db_librarians = DataBaseLibrarians()
    db_daytime = DataBaseTimetable()
    db_ordering = DataBaseOrders()
    app = Main(root)
    app.pack()
    root.title("Tiny Library")
    root.geometry("1250x700+180+70")
    # root.protocol('WM_DELETE_WINDOW', window_deleted)
    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()
