import pytest
from src.bibliotheque.user import User
from src.bibliotheque.book import Book

def test_create_valid_user():
    user = User("Nom", "email@mail.com")
    assert user.name == "Nom"
    assert user.email == "email@mail.com"

def test_invalid_email_raises_error():
    with pytest.raises(ValueError):
        User("Nom", "email")

def test_empty_name_raises_error():
    with pytest.raises(ValueError):
        User("", "email@mail.com")

def test_can_borrow_limit():
    user = User("Nom", "email@mail.com")
    assert user.can_borrow()
    book = Book("Titre", "Auteur", "1234567890123")
    user.add_borrowed_book(book)
    user.add_borrowed_book(book)
    user.add_borrowed_book(book)
    assert not user.can_borrow()
