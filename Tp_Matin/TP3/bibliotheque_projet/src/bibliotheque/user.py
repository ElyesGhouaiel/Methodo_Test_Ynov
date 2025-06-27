class User:
    """Représente un utilisateur de la bibliothèque"""

    def __init__(self, name, email):
        if not name:
            raise ValueError("Le nom ne doit pas être vide")
        if "@" not in email:
            raise ValueError("L'email doit contenir '@'")
        self.name = name
        self.email = email
        self.borrowed_books = []

    def can_borrow(self, max_books=3):
        return len(self.borrowed_books) < max_books

    def add_borrowed_book(self, book):
        self.borrowed_books.append(book)

    def remove_borrowed_book(self, book):
        self.borrowed_books.remove(book)
