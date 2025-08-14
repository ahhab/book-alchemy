from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an Author in the database.

    Attributes:
        id (int): Primary Key, auto-incrementing.
        name (str): The full name of the author. Cannot be null.
        birth_date (date): The birth date of the author. Can be null.
        date_of_death (date): The date of death of the author. Can be null.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # Define the relationship to Book: an author can have many books
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Author object.
        """
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Provides a user-friendly string representation of the Author object.
        """
        birth_str = self.birth_date.strftime(
            '%Y-%m-%d') if self.birth_date else 'N/A'
        death_str = self.date_of_death.strftime(
            '%Y-%m-%d') if self.date_of_death else 'N/A'
        return f"Author: {self.name} (Born: {birth_str}, Died: {death_str})"


class Book(db.Model):
    """
    Represents a Book in the database.

    Attributes:
        id (int): Primary Key, auto-incrementing.
        isbn (str): The International Standard Book Number. Unique.
        title (str): The title of the book. Cannot be null.
        publication_year (int): The year the book was published.
        author_id (int): Foreign Key to the Author table. Cannot be null.
    """
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id'), nullable=False)

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Book object.
        """
        return f"<Book(id={self.id}, title='{self.title}', author_id={self.author_id})>"

    def __str__(self):
        """
        Provides a user-friendly string representation of the Book object.
        """
        author_name = self.author.name if self.author else 'Unknown Author'
        return f"Book: '{self.title}' (ISBN: {self.isbn}, Published: {self.publication_year}) by {author_name}"
