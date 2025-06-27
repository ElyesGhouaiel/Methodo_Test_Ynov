from .book import Book
from .user import User

class Library:
    """Gestionnaire de bibliothèque"""

    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def borrow_book(self, user, isbn):
        book = self.find_book_by_isbn(isbn)
        if not book or not user.can_borrow() or not book.is_available():
            return False
        if book.borrow():
            user.add_borrowed_book(book)
            return True
        return False
