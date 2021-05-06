'''from tkinter import *
root = Tk()
text = Text(root, height=3, width=60)
text.pack(side='left')
scrollbar = Scrollbar(root)
scrollbar.pack(side='left')
# первая привязка
scrollbar['command'] = text.yview
# вторая привязка
text['yscrollcommand'] = scrollbar.set
root.mainloop()

from tkinter import *Ф
from tkinter import messagebox

root = Tk()

def btn_click():
    login = loginInput.get()
    password = passwordInput.get()

    info_str = f'Дані: {str(login)}, {str(password)}'
    messagebox.showinfo(title='Name', message=info_str)

    #вікно з помилкою
    #messagebox.showerror(title='', message='Error')


root['bg'] = '#E9BB7B'
self.title('Tiny Library')
self.geometry('450x250')

self.resizable(False, False)

self.canvas = Canvas(root, height=250, width=300)
self.canvas.pack()

self.frame = Frame(root, bg='#79350B')
self.frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)

self.title = Label(frame, text='Вхід до бібліотеки', bg='#C38661', font=40)
self.title.pack()

self.loginInput = Entry(frame, text='login',  bg='#F9E7DD')
self.loginInput.pack()
self.passwordInput = Entry(frame, bg='#F9E7DD', show='@')
self.passwordInput.pack()

self.btn = Button(frame, text='Log in', bg='#79350B', command=btn_click)
self.btn.pack()
icons8-160.png
self.mainloop()'''

from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title('test')

nb = ttk.Notebook(root)
nb.pack(fill='both', expand='yes')

f1 = Text(root)
f2 = Text(root)
f3 = Text(root)

nb.add(f1, text='page1')
nb.add(f2, text='page2')
nb.add(f3, text='page3')

root.mainloop()