import pytest
from src.bibliotheque.book import Book

@pytest.fixture
def sample_book():
    return Book("Titre", "Auteur", "1234567890123")

class TestBookCreation:
    """Tests de création de livre"""

    def test_create_valid_book(self, sample_book):
        assert sample_book.title == "Titre"
        assert sample_book.author == "Auteur"
        assert sample_book.isbn == "1234567890123"
        assert sample_book.is_available()

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

    def test_new_book_is_available(self, sample_book):
        assert sample_book.is_available()

    def test_borrow_available_book_success(self, sample_book):
        assert sample_book.borrow() is True
        assert not sample_book.is_available()

    def test_borrow_already_borrowed_book_fails(self, sample_book):
        sample_book.borrow()
        assert sample_book.borrow() is False

    def test_return_book_not_borrowed_fails(self, sample_book):
        assert sample_book.return_book() is False

    def test_return_borrowed_book_success(self, sample_book):
        sample_book.borrow()
        assert sample_book.return_book() is True
        assert sample_book.is_available()
