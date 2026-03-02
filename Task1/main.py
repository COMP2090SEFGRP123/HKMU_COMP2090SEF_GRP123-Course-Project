from tkinter import *

def search_books(self, query):
        found_books = []
        
        for book in self.books:
            if str(book.id) == query or book.title.lower() == query.lower(): # check if query matches id or title
                found_books.append(book)

def search():
    query = search_entry.get()
    results_list.delete(0, END) # clear previous results in the list
    results = library.search_books(query)
    
    if not results:
        results_list.insert(END, "No books found.")
    else:
        for book in results:
            results_list.insert(END, str(book))

def act():
    book_id = id_entry.get()
    action = act_var.get() # 1 or 0
    
    if action == 1:
        msg = library.borrow_book(book_id)
    else:
        msg = library.return_book(book_id)
        
    status_label.config(text=msg)
    search() # refresh the search to show updated info

root = Tk()
title = Label(root, text='Libary Manage System')
title.pack()
#search
Label(root, text="--- SEARCH BOOKS ---").pack()
Label(root, text="Enter Title or Book ID:").pack()
search_entry = Entry(root)
search_entry.pack()

Button(root, text="Search", command=search).pack
results_list = Listbox(root)
results_list.pack
root.mainloop()
