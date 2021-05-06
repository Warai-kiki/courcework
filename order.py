import tkinter as tk
from tkinter import ttk
import sqlite3
# розклад роботи
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_order = db_ordering
        self.view_orders()

    def init_main(self):
        toolbar = tk.Frame(bg='#EAC38D', bd=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        '''# entering in the system
        self.add_img_2 = tk.PhotoImage(file='enter-2.png')  # adding button pic
        btn_open_adding = tk.Button(toolbar, text='Вхід', command=self.open_login, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img_2)
        btn_open_adding.pack(side=tk.LEFT)'''

        # adding book button pic
        self.add_img = tk.PhotoImage(file='icons8-160.png')  # adding button pic
        btn_open_adding = tk.Button(toolbar, text='Додати книгу', command=self.open_add_order, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_adding.pack(side=tk.LEFT)
        # update button
        self.update_img = tk.PhotoImage(file='edit_160_2.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редагувати', bg='#D19440', bd=1, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog_order)
        btn_edit_dialog.pack(side=tk.LEFT)
        # delete button
        self.delete_img = tk.PhotoImage(file='delete_160.png')
        btn_delete = tk.Button(toolbar, text='Видалити', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_order)
        btn_delete.pack(side=tk.LEFT)
        # searching
        self.search_stat_img = tk.PhotoImage(file='search_80.png')
        btn_search_stat = tk.Button(toolbar, text='Пошук\nзаборгованостей', bg='#D19440', bd=1, image=self.search_stat_img,
                                    compound=tk.TOP, command=self.open_search_by_status)
        btn_search_stat.pack(side=tk.RIGHT)
        # searching readers
        self.search_peop_img = tk.PhotoImage(file='author_search_80.png')
        btn_search_date = tk.Button(toolbar, text='Пошук\nчитача', bg='#D19440', bd=1, image=self.search_peop_img,
                                    compound=tk.TOP, command=self.open_search_dialog_order)
        btn_search_date.pack(side=tk.RIGHT)
        #
        self.search_date_img = tk.PhotoImage(file='icons8-поиск-в-списке-80.png')
        btn_search_date = tk.Button(toolbar, text='Пошук по даті\nвидачі', bg='#D19440', bd=1, image=self.search_date_img,
                                    compound=tk.TOP, command=self.open_search_by_dates)
        btn_search_date.pack(side=tk.RIGHT)
        # refreshing button
        self.refrech_img = tk.PhotoImage(file='refresh_80.png')
        btn_refresh = tk.Button(toolbar, text='Оновити\n', bg='#D19440', bd=1, image=self.refrech_img,
                                compound=tk.TOP, command=self.view_orders)
        btn_refresh.pack(side=tk.RIGHT)

        # table
        self.tree = ttk.Treeview(self, column=('ID', 'name', 'book', 'user_id', 'took', 'need_return', 'status'), height=30,
                                 show='headings')

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('book', width=250, anchor=tk.CENTER)
        self.tree.column('user_id', width=150, anchor=tk.CENTER)
        self.tree.column('took', width=120, anchor=tk.CENTER)
        self.tree.column('need_return', width=120, anchor=tk.CENTER)
        self.tree.column('status', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Читач')
        self.tree.heading('book', text='Книга/Журнал')
        self.tree.heading('user_id', text='ID користувача')
        self.tree.heading('took', text='Дата видачі')
        self.tree.heading('need_return', text='Дата повернення')
        self.tree.heading('status', text='Статус')


        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def orders(self, name, book, user_id, took, need_return, status):
        self.db_order.insert_order(name, book, user_id, took, need_return, status)
        self.view_orders()

    def view_orders(self):
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders''')
        [self.tree.delete(i) for i in self.tree.get_children()] # отображение на экране
        [self.tree.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def update_order(self, name, book, user_id, took, need_return, status):
        self.db_order.db_orders.execute('''UPDATE orders SET name, book, user_id, took, need_return, status WHERE id=?''',
                                        (name, book, user_id, took, need_return, status, self.tree.set(self.tree.selection()[0], '#1')))
        self.db_order.db_orders.commit()
        self.view_orders()

    def delete_order(self):
        for selection_item in self.tree.selection():
            self.db_order.db_orders.execute('''DELETE FROM orders WHERE ID=?''', (self.tree.set(selection_item, '#1')))
        self.db_order.db_orders.commit()
        self.view_orders()

    def search_in_ord_catalog(self, name):
        name = ('%' + name + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def search_among_orders_status(self, status):
        status = ('%' + status + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE author LIKE ?''', status)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def search_among_dates(self, date):
        date = ('%' + date + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE took LIKE ?''', date)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

    def search_among_need_to_back(self, date):
        date = ('%' + date + '%',)
        self.db_order.db_orders_conn.execute('''SELECT * FROM orders WHERE need_return LIKE ?''', date)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_order.db_orders_conn.fetchall()]

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
        self.db_daytime = db_ordering
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
        self.db_daytime.db_orders_conn.execute('''SELECT * FROM orders WHERE ID=?''',
                                               (self.view.tree.set(self.view.tree.selection()[0],'#1')))
        row = self.db_daytime.db_orders_conn.fetchone()
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

        #self.title = tk.Label(self.frame, text='Пошук', bg='#C38661', font=40)
        #self.title.pack()

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

if __name__ == "__main__":
    root = tk.Tk()
    db_ordering = DataBaseOrders()
    app = Main(root)
    app.pack()
    root.title("Tiny Library")
    root.geometry("1250x700+180+70")
    # root.protocol('WM_DELETE_WINDOW', window_deleted)
    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()