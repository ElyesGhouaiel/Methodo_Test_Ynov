import pytest
from src.bibliotheque.book import Book

class TestBookCreation:
    """Tests de création de livre"""

    def test_create_valid_book(self):
        book = Book("Titre", "Auteur", "1234567890123")
        assert book.title == "Titre"
        assert book.author == "Auteur"
        assert book.isbn == "1234567890123"
        assert book.is_available()

    def test_create_book_empty_title_raises_error(self):
        with pytest.raises(ValueError):
            Book("", "Auteur", "1234567890123")

    def test_create_book_invalid_isbn_raises_error(self):
        with pytest.raises(ValueError):
            Book("Titre", "Auteur", "123")
        with pytest.raises(ValueError):
            Book("Titre", "Auteur", "12345678901234")

class TestBookBorrowing:
    """Tests d'emprunt de livre"""

    def setup_method(self):
        self.book = Book("Titre", "Auteur", "1234567890123")

    def test_new_book_is_available(self):
        assert self.book.is_available()

    def test_borrow_available_book_success(self):
        assert self.book.borrow() is True
        assert not self.book.is_available()

    def test_borrow_already_borrowed_book_fails(self):
        self.book.borrow()
        assert self.book.borrow() is False

    def test_return_book_not_borrowed_fails(self):
        assert self.book.return_book() is False

    def test_return_borrowed_book_success(self):
        self.book.borrow()
        assert self.book.return_book() is True
        assert self.book.is_available()
