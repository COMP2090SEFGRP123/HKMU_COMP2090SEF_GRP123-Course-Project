import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

from models import Admin, Student, Book
from system import LibrarySystem

class LibraryGUI:
    def __init__(self, root, library_system):
        self.root = root
        self.library = library_system
        self.current_user = None
        self.users = {}

        self.root.title("Library Management System")
        self.root.geometry("1050x680")
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #======login======
    def load_users(self):
        if os.path.exists("users.json"):
            try:
                with open("users.json", "r") as f:
                    self.users = json.load(f)
            except:
                self.users = {}

    def save_users(self):
        try:
            with open("users.json", "w") as f:
                json.dump(self.users, f, indent=4)
        except:
            pass

    def show_login_screen(self):
        self.clear_window()#clear the window when switching between login and dashboard
        self.load_users()

        frame = tk.Frame(self.root, padx=40, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="Library Management System", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(frame, text="Login", font=("Arial", 12)).pack(pady=10)

        tk.Label(frame, text="User ID:").pack(anchor="w")
        self.entry_id = tk.Entry(frame, width=35)
        self.entry_id.pack(pady=5)

        tk.Label(frame, text="Password:").pack(anchor="w")
        self.entry_password = tk.Entry(frame, width=35)
        self.entry_password.pack(pady=5)

        tk.Button(frame, text="Login", command=self.login, width=20).pack(pady=20)

    def login(self):
        userid = self.entry_id.get().strip().lower()
        password = self.entry_password.get().strip()

        if not userid or not password:
            messagebox.showerror("Error", "Please fill User ID and Password.")
            return

        prefix = userid[0] if userid else ""
        if prefix not in ['a', 's']:
            messagebox.showerror("Error", "User ID must start with 'a' or 's'.")
            return

        role = "admin" if prefix == "a" else "student"

        if userid in self.users:
            if self.users[userid]["password"] != password:
                messagebox.showerror("Error", "Incorrect password!")
                return
        else:
            self.users[userid] = {"password": password, "role": role}
            self.save_users()
            messagebox.showinfo("Success", f"New {role.capitalize()} account created!")

        if role == "admin":
            self.ask_admin_password(userid)
        else:
            self.current_user = Student(userid, userid)
            self.show_dashboard()

    def ask_admin_password(self, userid):
        top = tk.Toplevel(self.root)
        top.title("Admin Verification")
        top.geometry("380x200")
        top.grab_set()

        tk.Label(top, text="Admin Verification", font=("Arial", 14, "bold")).pack(pady=15)
        tk.Label(top, text="Please enter the Admin Password", fg="red").pack(pady=5)

        admin_pass_entry = tk.Entry(top, width=30, font=("Arial", 11))
        admin_pass_entry.pack(pady=10)
        admin_pass_entry.focus()

        def verify_admin():
            if admin_pass_entry.get().strip() == "admin1454":
                top.destroy()
                self.current_user = Admin(userid, userid)
                self.show_dashboard()
            else:
                messagebox.showerror("Access Denied", "Incorrect Admin Password!")
                top.destroy()

        tk.Button(top, text="Verify", command=verify_admin, width=15, height=2).pack(pady=10)
        admin_pass_entry.bind("<Return>", lambda event: verify_admin())

    #======dashboard======
    def show_dashboard(self):
        self.clear_window()

        header = tk.Frame(self.root, pady=10)
        header.pack(fill="x", padx=15)
        role_text = "Admin" if isinstance(self.current_user, Admin) else "Student"
        tk.Label(header, text=f"Welcome, {self.current_user.name} ({role_text})", 
                 font=("Arial", 12, "bold")).pack(side="left")
        tk.Button(header, text="Logout", command=self.show_login_screen).pack(side="right")

        search_frame = tk.LabelFrame(self.root, text="Search Books", padx=10, pady=8)
        search_frame.pack(fill="x", padx=10)

        self.search_var = tk.StringVar(value="Title")
        tk.Radiobutton(search_frame, text="Title", variable=self.search_var, value="Title").pack(side="left")
        tk.Radiobutton(search_frame, text="Book ID", variable=self.search_var, value="BookID").pack(side="left", padx=15)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=10)

        tk.Button(search_frame, text="Search", command=self.perform_search).pack(side="left")
        tk.Button(search_frame, text="Show All", command=self.show_all_books).pack(side="left", padx=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("BookID", "Title", "Author", "Status", "DueDate")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("BookID", text="Book ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Status", text="Status")
        self.tree.heading("DueDate", text="Due Date")

        self.tree.column("BookID", width=90)
        self.tree.column("Title", width=300)
        self.tree.column("Author", width=160)
        self.tree.column("Status", width=100)
        self.tree.column("DueDate", width=130)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self.root, pady=8)
        btn_frame.pack(fill="x", padx=10)

        if isinstance(self.current_user, Admin):
            tk.Button(btn_frame, text="Borrow Selected", command=self.borrow_action).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Return Selected", command=self.return_action).pack(side="left", padx=5)

            admin_frame = tk.LabelFrame(self.root, text="Admin Controls", padx=10, pady=8, fg="red")
            admin_frame.pack(fill="x", padx=10, pady=5)
            tk.Button(admin_frame, text="Add New Book", command=self.open_add_book_window).pack(side="left", padx=5)
            tk.Button(admin_frame, text="Delete Selected", command=self.delete_book_action, bg="red", fg="white").pack(side="left", padx=5)

        self.show_all_books()

    #======gui======
    def update_table(self, books):
        for item in self.tree.get_children():
            self.tree.delete(item)

        today = datetime.now().date()
        for book in books:
            status = "Borrowed" if book.is_borrowed else "Available"
            due_str = book.due_date.strftime("%Y-%m-%d") if book.due_date else "N/A"
            item_id = self.tree.insert("", "end", values=(book.book_id, book.title, book.author, status, due_str))
            
            if book.is_borrowed and book.due_date and book.due_date < today:
                self.tree.item(item_id, tags=("overdue",))

        self.tree.tag_configure("overdue", foreground="red")

    def get_selected_book_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first!")
            return None
        return self.tree.item(selected[0])['values'][0]

    def perform_search(self):
        query = self.search_entry.get().strip()
        if not query:
            self.show_all_books()
            return

        if self.search_var.get() == "BookID":
            book = self.library.find_book_by_id(query)
            results = [book] if book else []
        else:
            results = self.library.find_books_by_title(query)
        self.update_table(results)

    def show_all_books(self):
        self.update_table(self.library.get_all_books())

    #======short action======
    def borrow_action(self):
        book_id = self.get_selected_book_id()
        if book_id:
            success, msg = self.library.borrow_book(book_id)
            messagebox.showinfo("Borrow", msg)
            self.show_all_books()

    def return_action(self):
        book_id = self.get_selected_book_id()
        if book_id:
            success, msg = self.library.return_book(book_id)
            messagebox.showinfo("Return", msg)
            self.show_all_books()

    def delete_book_action(self):
        book_id = self.get_selected_book_id()
        if book_id and messagebox.askyesno("Confirm", "Delete this book?"):
            success, msg = self.library.remove_book_by_id(book_id)
            messagebox.showinfo("Delete", msg)
            self.show_all_books()

    def open_add_book_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Book")
        top.geometry("320x220")

        tk.Label(top, text="Title:").pack(pady=5)
        e_title = tk.Entry(top, width=35); e_title.pack()

        tk.Label(top, text="Author:").pack(pady=5)
        e_author = tk.Entry(top, width=35); e_author.pack()

        tk.Label(top, text="Book ID:").pack(pady=5)
        e_book_id = tk.Entry(top, width=35); e_book_id.pack()

        def add_book():
            title = e_title.get().strip()
            author = e_author.get().strip()
            book_id = e_book_id.get().strip()

            if not all([title, author, book_id]):
                messagebox.showerror("Error", "All fields are required!")
                return

            new_book = Book(title, author, book_id)
            success, msg = self.library.add_book(new_book)
            messagebox.showinfo("Add Book", msg)
            if success:
                self.show_all_books()
                top.destroy()

        tk.Button(top, text="Add Book", command=add_book).pack(pady=15)
