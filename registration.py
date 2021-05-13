import tkinter as tk
from tkinter import ttk
import sqlite3

class Autorisation(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_readers = db_readers
        self.db_librarians = db_librarians
        self.view_librarians()
        self.view_readers()


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

        # adding button for librarians
        self.add_img = tk.PhotoImage(file='icons8-160.png')  # adding button pic
        btn_open_adding = tk.Button(self.tab_1_lib, text='Додати\nбібліотекаря', command=self.open_adding_libs, bg='#D19440',
                                    bd=1,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_adding.place(x=0, y=4)
        # update button for librarians
        self.update_img = tk.PhotoImage(file='edit_160_2.png')
        btn_edit_dialog = tk.Button(self.tab_1_lib, text='Редагувати\nбібліотекаря', bg='#D19440', bd=1, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_librs)
        btn_edit_dialog.place(x=0, y=204)
        # delete button for librarians
        self.delete_img = tk.PhotoImage(file='delete_160.png')
        btn_delete = tk.Button(self.tab_1_lib, text='Видалити\nбібліотекаря', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_librarian)
        btn_delete.place(x=0, y=404)
        # searching for librarians
        self.search_people = tk.PhotoImage(file='author_search_80.png')
        btn_search = tk.Button(self.tab_1_lib, text='Пошук\nбібліотекаря', bg='#D19440', bd=1, image=self.search_people,
                               compound=tk.TOP, command=self.open_search_libr)
        btn_search.place(x=1160, y=4)
        # refreshing button for librarians
        self.refrech_img = tk.PhotoImage(file='refresh_80.png')
        btn_refresh_lib = tk.Button(self.tab_1_lib, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                compound=tk.TOP, command=self.view_librarians)
        btn_refresh_lib.place(x=1160, y=130)

        # update button for readers
        btn_edit_dialog_read = tk.Button(self.tab_2_lib, text='Редагувати\nчитача', bg='#D19440', bd=1,
                                    image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_readers)
        btn_edit_dialog_read.place(x=0, y=4)
        # delete button for readers
        btn_delete_reader = tk.Button(self.tab_2_lib, text='Видалити\nчитача', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_readers)
        btn_delete_reader.place(x=0, y=204)
        # searching for readers
        btn_search_reader = tk.Button(self.tab_2_lib, text='Пошук читача', bg='#D19440', bd=1, image=self.search_people,
                                      compound=tk.TOP, command=self.open_search_read)
        btn_search_reader.place(x=1160, y=4)
        # refreshing button for readers
        btn_refresh = tk.Button(self.tab_2_lib, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                compound=tk.TOP, command=self.view_readers)
        btn_refresh.place(x=1160, y=130)


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

    def readers(self, name, email, password):
        self.db_readers.insert_readers(name, email, password)
        self.view_readers()

    def view_readers(self):
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers''')
        [self.tree_readers.delete(i) for i in self.tree_readers.get_children()] # отображение на экране
        [self.tree_readers.insert('', 'end', values=row) for row in self.db_readers.db_readers_conn.fetchall()]

    def librarians(self, name, email, password):
        self.db_librarians.insert_librarians(name, email, password)
        self.view_librarians()

    def view_librarians(self):
        self.db_librarians.db_librarians_conn.execute('''SELECT * FROM librarians''')
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()] # отображение на экране
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_librarians.db_librarians_conn.fetchall()]

    def update_librarian(self, name, email, password):
        self.db_librarians.db_librarians_conn.execute('''UPDATE librarians SET name=?, email=?, password=?''',
                                         (name, email, password, self.tree_libras.set(self.tree_libras.selection()[0], '#1')))
        self.db_librarians.db_librarians_conn.commit()
        self.view_librarians()

    def delete_librarian(self):
        for selection_item in self.tree_libras.selection():
            self.db_librarians.db_librarians_conn.execute('''DELETE FROM librarians WHERE ID=?''', (self.tree_libras.set(selection_item, '#1')))
        self.db_librarians.db_librarians_conn.commit()
        self.view_librarians()

    def update_readers(self, name, email, password):
        self.db_readers.db_readers_conn.execute('''UPDATE readers SET name=?, email=?, password=?''',
                                         (name, email, password, self.tree_readers.set(self.tree_readers.selection()[0], '#1')))
        self.db_readers.db_readers_conn.commit()
        self.view_readers()

    def delete_readers(self):
        for selection_item in self.tree_readers.selection():
            self.db_readers.db_readers_conn.execute('''DELETE FROM readers WHERE ID=?''', (self.tree_readers.set(selection_item, '#1')))
        self.db_readers.db_readers_conn.commit()
        self.view_readers()

    def search_among_librarians(self, name):
        name = ('%' + name + '%',)
        self.db_librarians.db_librarians_conn.execute('''SELECT * FROM librarians WHERE name LIKE ?''', name)
        [self.tree_libras.delete(i) for i in self.tree_libras.get_children()]
        [self.tree_libras.insert('', 'end', values=row) for row in self.db_librarians.db_librarians_conn.fetchall()]

    def search_among_readers(self, name):
        name = ('%' + name + '%',)
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers WHERE name LIKE ?''', name)
        [self.tree_readers.delete(i) for i in self.tree_readers.get_children()]
        [self.tree_readers.insert('', 'end', values=row) for row in self.db_readers.db_readers_conn.fetchall()]

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
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_librarians(self.entry_search_2.get()))
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
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_readers(self.entry_search_2.get()))
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
        self.btn_add.bind('<Button-1>', lambda event: self.view.librarians(self.entry_name.get(), self.entry_email.get(),
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
        btn_edit.bind('<Button>', lambda event: self.view.update_librarian(self.entry_name.get(), self.entry_email.get(),
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
        btn_edit.bind('<Button>', lambda event: self.view.update_readers(self.entry_name.get(), self.entry_email.get(),
                                                                           self.entry_password.get()))
        self.btn_add.destroy()

    def default_data(self):
        self.db_readers.db_readers_conn.execute('''SELECT * FROM readers WHERE ID=?''',
                                                 (self.view.tree_readers.set(self.view.tree_readers.selection()[0],'#1')))
        row = self.db_readers.db_readers_conn.fetchone()
        self.entry_name.insert(0,row[1])



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

if __name__ == "__main__":
    root = tk.Tk()
    db_readers = DataBaseReaders()
    db_librarians = DataBaseLibrarians()
    app = Autorisation(root)
    app.pack()
    root.title("Контроль акаунтів")
    root.geometry("1250x700+180+70")

    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()