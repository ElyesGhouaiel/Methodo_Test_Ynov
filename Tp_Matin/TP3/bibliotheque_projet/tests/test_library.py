import pytest
from src.bibliotheque.library import Library
from src.bibliotheque.book import Book
from src.bibliotheque.user import User

class TestLibraryOperations:

    def setup_method(self):
        self.library = Library("Médiathèque")
        self.book1 = Book("Livre 1", "Auteur 1", "1111111111111")
        self.book2 = Book("Livre 2", "Auteur 2", "2222222222222")
        self.book3 = Book("Livre 3", "Auteur 3", "3333333333333")
        self.user = User("Alice", "alice@mail.com")
        self.user2 = User("Bob", "bob@mail.com")
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)

    def test_borrow_flow_success(self):
        success = self.library.borrow_book(self.user, "1111111111111")
        assert success
        assert not self.book1.is_available()
        assert self.book1 in self.user.borrowed_books

    def test_user_cannot_borrow_more_than_limit(self):
        self.library.borrow_book(self.user, "1111111111111")
        self.library.borrow_book(self.user, "2222222222222")
        self.library.borrow_book(self.user, "3333333333333")
        book4 = Book("Livre 4", "Auteur 4", "4444444444444")
        self.library.add_book(book4)
        assert self.library.borrow_book(self.user, "4444444444444") is False
