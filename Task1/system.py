class LibrarySystem:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print("Added:", book._title)

    def remove_book(self, title):
        for book in self.books:
            if book._title == title:
                self.books.remove(book)
                print("Removed:", title)
                return
        print("Cannot find this book.")

    def search_book(self, title):
        for book in self.books:
            if book._title == title:
                print("Found:", book)
                return book
        print("Book not found.")
        return None

    def borrow_book(self, title):
        for book in self.books:
            if book._title == title:
                if book._borrowed:
                    print("This book is already borrowed.")
                else:
                    book.borrow()
                    print("You borrowed:", title)
                return
        print("Book not found.")

    def return_book(self, title):
        for book in self.books:
            if book._title == title:
                if not book._borrowed:
                    print("This book was not borrowed.")
                else:
                    book.return_book()
                    print("Returned:", title)
                return
        print("Book not found.")

    def show_all_books(self):
        if len(self.books) == 0:
            print("No books in library.")
            return

        print("All books:")
        for book in self.books:
            print(book)

    def total_books(self):
        return len(self.books)
