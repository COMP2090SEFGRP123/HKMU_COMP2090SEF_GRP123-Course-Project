import json
import os
from models import Book

class LibrarySystem:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, book):
        if self.find_book_by_id(book.book_id):
            return False, "Book ID already exists!"
        self.books.append(book)
        self.save_books()
        return True, "Book added successfully."

    def remove_book_by_id(self, book_id):
        for book in self.books[:]:
            if book.book_id == str(book_id):
                self.books.remove(book)
                self.save_books()
                return True, "Book removed successfully."
        return False, "Book not found."

    def borrow_book(self, book_id):
        book = self.find_book_by_id(book_id)
        if not book:
            return False, "Book not found."
        success, msg = book.borrow()
        if success:
            self.save_books()
        return success, msg

    def return_book(self, book_id):
        book = self.find_book_by_id(book_id)
        if not book:
            return False, "Book not found."
        success, msg = book.return_book()
        if success:
            self.save_books()
        return success, msg

    def get_all_books(self):
        return self.books

    def find_book_by_id(self, book_id):
        book_id = str(book_id).strip()
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_books_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    #memory(?) part, so the list wouldnt clear after close
    def save_books(self):
        try:
            data = [book.to_dict() for book in self.books]
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Error saving books:", e)

    def load_books(self):
        if not os.path.exists("books.json"):
            return
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book.from_dict(item) for item in data]
        except Exception as e:
            print("Error loading books:", e)
            self.books = []

    def add_sample_books(self):
        if len(self.books) == 0:
            self.add_book(Book("Python Basics", "John Doe", "101"))
            self.add_book(Book("Advanced Math", "Jane Smith", "102"))
            self.add_book(Book("History of Art", "Bob Ross", "103"))
            print("Sample books added.")
