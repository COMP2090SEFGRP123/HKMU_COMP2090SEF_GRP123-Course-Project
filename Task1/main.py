from tkinter import *

root = Tk()
title = Label(root, text='Libary Manage System')
title.pack()
action = Label(root, text='Enter 1 to borrow, enter 0 to return')
action.pack()
user_act = Entry(root)
user_act.pack()
button = Button(root, text='Request', command=act)

root.mainloop()
