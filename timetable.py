import tkinter as tk
from tkinter import ttk
import sqlite3

# розклад роботи
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db_daytime = db_daytime
        self.view_timetable()
        #self.tabs_conrol = ttk.Notebook(self, root)

    def init_main(self):
        toolbar = tk.Frame(bg='#EAC38D', bd=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        '''# entering in the system
        self.add_img_2 = tk.PhotoImage(file='enter-2.png')  # adding button pic
        btn_open_adding = tk.Button(toolbar, text='Вхід', command=self.open_login, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img_2)
        btn_open_adding.pack(side=tk.LEFT)'''

        # adding book to timetable
        self.add_img = tk.PhotoImage(file='icons8-160.png')  # adding button pic
        btn_open_adding = tk.Button(toolbar, text='Додати бібліотекаря', command=self.open_add_libro, bg='#D19440', bd=1,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_adding.pack(side=tk.LEFT)
        # update button to timetable
        self.update_img = tk.PhotoImage(file='edit_160_2.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редагувати', bg='#D19440', bd=1, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog_libr)
        btn_edit_dialog.pack(side=tk.LEFT)
        # delete button to timetable
        self.delete_img = tk.PhotoImage(file='delete_160.png')
        btn_delete = tk.Button(toolbar, text='Видалити', bg='#D19440', bd=1, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_libros)
        btn_delete.pack(side=tk.LEFT)

        # searching librarian to timetable
        self.search_au_img = tk.PhotoImage(file='author_search_80.png')
        btn_search_auth = tk.Button(toolbar, text='Пошук бібліотекаря', bg='#D19440', bd=1, image=self.search_au_img,
                               compound=tk.TOP, command=self.open_search_dialog_libr)
        btn_search_auth.pack(side=tk.RIGHT)
        # refreshing button to timetable
        self.refrech_img = tk.PhotoImage(file='refresh_80.png')
        btn_refresh = tk.Button(toolbar, text='Оновити', bg='#D19440', bd=1, image=self.refrech_img,
                                    compound=tk.TOP, command=self.view_timetable)
        btn_refresh.pack(side=tk.RIGHT)

        # table to timetable
        self.tree_time = ttk.Treeview(self, column=('ID', 'name', 'monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday'), height=30,
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

    def delete_libros(self):
        for selection_item in self.tree_time.selection():
            self.db_daytime.db_timetable.execute('''DELETE FROM timetable WHERE ID=?''', (self.tree_time.set(selection_item, '#1')))
        self.db_daytime.db_timetable.commit()
        self.view_timetable()

    def search_among_librarians(self, author):
        author = ('%' + author + '%',)
        self.db_daytime.db_timetable_conn.execute('''SELECT * FROM timetable WHERE author LIKE ?''', author)
        [self.tree_time.delete(i) for i in self.tree_time.get_children()]
        [self.tree_time.insert('', 'end', values=row) for row in self.db_daytime.db_timetable_conn.fetchall()]

    def open_add_libro(self):
        AddTimeLib()

    def open_update_dialog_libr(self):
        UpdateTimeInfo()

    def open_search_dialog_libr(self):
        SearchLibrarians()

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
class SearchLibrarians(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.geometry('300x100+400+300')
        self.resizable(False,False)

        #self.title = tk.Label(self.frame, text='Пошук', bg='#C38661', font=40)
        #self.title.pack()

        label_search = tk.Label(self, text='Пошук бібліотекаря')
        label_search.place(x=10, y=20)

        self.entry_search_2 = ttk.Entry(self)
        self.entry_search_2.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_among_librarians(self.entry_search_2.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

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
    db_daytime = DataBaseTimetable()
    app = Main(root)
    app.pack()
    root.title("Tiny Library")
    root.geometry("1250x700+180+70")
    # root.protocol('WM_DELETE_WINDOW', window_deleted)
    root.resizable(False, False)
    root.iconbitmap("library_3978.ico")
    root.mainloop()
