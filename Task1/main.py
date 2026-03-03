import tkinter as tk
from tkinter import ttk, messagebox
from models import *
from system import *
class LibraryGUI:
    def __init__(self, root, library_system):
        self.root = root
        self.library = library_system
        self.current_user = None
        
        self.root.title("Library Management System")
        self.root.geometry("900x600")
        
        # Start at Login Screen
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #login

    def show_login_screen(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Library Login").pack(pady=10)
    #input
        # name
        tk.Label(frame, text="Name:").pack(anchor="w")
        self.entry_name = tk.Entry(frame, width=30)
        self.entry_name.pack(pady=5)

        #id
        tk.Label(frame, text="User ID:").pack(anchor="w")
        self.entry_id = tk.Entry(frame, width=30)
        self.entry_id.pack()

        #role
        tk.Label(frame, text="Role (Type 'admin' or 'student'):").pack(anchor="w", pady=(10, 0))
        self.entry_role = tk.Entry(frame, width=30)
        self.entry_role.pack(pady=5)

        tk.Button(frame, text="Login", command=self.login, width=20).pack(pady=20)
    #might add verify for login in the future so having name and userid here
    def login(self):
        name = self.entry_name.get().strip()
        userid = self.entry_id.get().strip()
        role_input = self.entry_role.get().strip().lower() 
        if not name or not userid or not role_input:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if role_input == "admin":
            self.current_user = Admin(name, userid)
            self.current_user = Student(name, userid)
        else:
            messagebox.showerror("Error", "Invalid Role. Please type 'admin' or 'student'.")
            return
        self.showdashboard()

    #dashboard

    def showdashboard(self):
        self.clear_window()

        #head
        header_frame = tk.Frame(self.root, pady=10, padx=10)
        header_frame.pack(fill="x")

        #show user name and role
        role_display = "Admin" if isinstance(self.current_user, Admin) else "Student"
        tk.Label(header_frame, text=f"Welcome, {self.current_user.name} ({role_display})").pack(side="left")
        
        #logout
        tk.Button(header_frame, text="Logout", command=self.show_login_screen).pack(side="right")

        #search
        search_frame = tk.LabelFrame(self.root, text="Search Books", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar(value="Title")
        tk.Radiobutton(search_frame, text="Title", variable=self.search_var, value="Title").pack(side="left", padx=5)
        tk.Radiobutton(search_frame, text="ID/ISBN", variable=self.search_var, value="ISBN").pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=10)
        
        tk.Button(search_frame, text="Search", command=self.perform_search).pack(side="left")
        tk.Button(search_frame, text="Show All", command=self.show_all_books).pack(side="left", padx=5)

        #show result
        result_frame = tk.Frame(self.root)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ISBN", "Title", "Author", "Status")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        self.tree.heading("ISBN", text="Book ID / ISBN")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Status", text="Status")

        self.tree.column("ISBN", width=100)
        self.tree.column("Title", width=250)
        self.tree.column("Author", width=150)
        self.tree.column("Status", width=100)

        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        #action
        action_frame = tk.Frame(self.root, pady=10)
        action_frame.pack(fill="x", padx=10)

        tk.Button(action_frame, text="Borrow Selected", command=self.borrow_action).pack(side="left", padx=5)
        tk.Button(action_frame, text="Return Selected", command=self.return_action).pack(side="left", padx=5)

        #admin part
        if isinstance(self.current_user, Admin):
            admin_frame = tk.LabelFrame(self.root, text="Admin Controls", padx=10, pady=10, fg="red")
            admin_frame.pack(fill="x", padx=10, pady=10)
            
            tk.Button(admin_frame, text="Add New Book", command=self.open_add_book_window).pack(side="left", padx=5)
            tk.Button(admin_frame, text="Delete Selected Book", command=self.delete_book_action, bg="red", fg="white").pack(side="left", padx=5)

        # Load initial data
        self.show_all_books()

    # LOGIC METHODS

    def update(self, books):
        """Updates the list with the provided books."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for book in books:
            status = "Borrowed" if book.is_borrowed else "Available"
            self.tree.insert("", "end", values=(book.isbn, book.title, book.author, status))

    def get_selected_isbn(self):
        """Helper to get the ISBN of the currently selected row."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book from the list.")
            return None
        item_data = self.tree.item(selected_item[0])
        return item_data['values'][0] # ISBN is the first column

    def perform_search(self):
        query = self.search_entry.get().strip()
        search_type = self.search_var.get()
        
        if not query:
            self.show_all_books()
            return

        results = []
        if search_type == "ISBN":
            book = self.library.find_book_by_isbn(query)
            if book: results.append(book)
        elif search_type == "Title":
            results = self.library.find_books_by_title(query)
            
        self.update(results)

    def show_all_books(self):
        self.update(self.library.get_all_books())

    def borrow_action(self):
        isbn = self.get_selected_isbn()
        if not isbn: return
        book = self.library.find_book_by_isbn(str(isbn))
        
        if book:
            success, msg = self.current_user.borrow_book(book)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
            self.show_all_books() #refresh UI
        else:
            messagebox.showerror("Error", "Book not found.")

    def return_action(self):
        isbn = self.get_selected_isbn()
        if not isbn: return
        
        book = self.library.find_book_by_isbn(str(isbn))
        
        if book:
            success, msg = self.current_user.return_book(book)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
            self.show_all_books() #refresh UI
        else:
            messagebox.showerror("Error", "Book not found.")
    #admin
    def delete_book_action(self):
        isbn = self.get_selected_isbn()
        if not isbn: return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            book = self.library.find_book_by_isbn(str(isbn))
            if book:
                msg = self.current_user.remove_book_from_library(self.library, book)
                messagebox.showinfo("Admin Action", msg)
                self.show_all_books()

    def open_add_book_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Book")
        top.geometry("300x250")

        tk.Label(top, text="Title:").pack()
        e_title = tk.Entry(top)
        e_title.pack()

        tk.Label(top, text="Author:").pack()
        e_author = tk.Entry(top)
        e_author.pack()

        tk.Label(top, text="ISBN (ID):").pack()
        e_isbn = tk.Entry(top)
        e_isbn.pack()

        tk.Label(top, text="Year:").pack()
        e_year = tk.Entry(top)
        e_year.pack()

        def addbook():
            try:
                # Create new book object using imported class
                b = Book(e_title.get(), e_author.get(), e_isbn.get(), int(e_year.get()))
                msg = self.current_user.add_book_to_library(self.library, b)
                messagebox.showinfo("Success", msg)
                self.show_all_books()
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Year must be a number.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text="Add Book", command=addbook).pack(pady=10)

#test
if __name__ == "__main__":
    my_library = Library("City Public Library")
    my_library.add_book(Book("Python Basics", "John Doe", "101", 2020))
    my_library.add_book(Book("Advanced Math", "Jane Smith", "102", 2019))
    my_library.add_book(Book("History of Art", "Bob Ross", "103", 2021))

    root = tk.Tk()
    app = LibraryGUI(root, my_library)
    root.mainloop()
