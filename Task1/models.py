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
    def is_borrowed(self):
        return self._borrowed
