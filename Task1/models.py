class Book:
    def __init__(self, title, author, isbn, year):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._year = year
        self._borrowed = False

    def borrow(self):
        if not self._borrowed:
            self._borrowed = True
            print("Book borrowed successfully.")
        else:
            print("This book is already borrowed.")

    def return_book(self):
        if self._borrowed:
            self._borrowed = False
            print("Book returned.")
        else:
            print("This book was not borrowed.")

    def __str__(self):
        if self._borrowed:
            status = "Borrowed"
        else:
            status = "Available"
        return self._title + " by " + self._author + " (ISBN: " + self._isbn + ") - " + status

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def isbn(self):
        return self._isbn

    @property
    def year(self):
        return self._year

    @property
    def is_borrowed(self):
        return self._borrowed


class User:
    def __init__(self, name):
        self._name = name

    def get_role(self):
        return "User"

    def borrow_book(self, book):
        if book.is_borrowed:
            return False, "Book already borrowed."
        book.borrow()
        return True, "Book borrowed successfully."

    def return_book(self, book):
        if not book.is_borrowed:
            return False, "Book was not borrowed."
        book.return_book()
        return True, "Book returned successfully."


class Admin(User):
    def get_role(self):
        return "Admin"

    def add_book_to_library(self, library, book):
        library.add_book(book)
        return "Book added to library."

    def remove_book_from_library(self, library, book):
        if book in library.books:
            library.books.remove(book)
            return "Book removed from library."
        return "Book not found."
