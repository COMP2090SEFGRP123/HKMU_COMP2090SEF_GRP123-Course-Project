from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, book_id):
        self._title = title
        self._author = author
        self._book_id = book_id
        self._borrowed = False
        self._borrow_date = None
        self._due_date = None

    def borrow(self):
        if not self._borrowed:
            self._borrowed = True
            self._borrow_date = datetime.now().date()
            self._due_date = self._borrow_date + timedelta(days=14)
            return True, f"Book borrowed successfully!\nDue Date: {self._due_date}"
        return False, "Book already borrowed."

    def return_book(self):
        if self._borrowed:
            self._borrowed = False
            self._borrow_date = None
            self._due_date = None
            return True, "Book returned successfully."
        return False, "Book was not borrowed."

    def to_dict(self):
        return {
            "title": self._title,
            "author": self._author,
            "book_id": self._book_id,
            "borrowed": self._borrowed,
            "borrow_date": self._borrow_date.strftime("%Y-%m-%d") if self._borrow_date else None,
            "due_date": self._due_date.strftime("%Y-%m-%d") if self._due_date else None
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["book_id"])
        book._borrowed = data.get("borrowed", False)
        if data.get("borrow_date"):
            book._borrow_date = datetime.strptime(data["borrow_date"], "%Y-%m-%d").date()
        if data.get("due_date"):
            book._due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        return book

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def book_id(self):
        return self._book_id

    @property
    def is_borrowed(self):
        return self._borrowed

    @property
    def due_date(self):
        return self._due_date

class User:
    def __init__(self, name, userid):
        self._name = name
        self._userid = userid

    @property
    def name(self):
        return self._name

class Admin(User):
    pass

class Student(User):
    pass
