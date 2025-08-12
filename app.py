from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests
from data_models import db, Author, Book
from datetime import datetime

# 1. Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key' # Needed for flashing messages

# 2. Configure the database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to suppress a warning

# 3. Initialize SQLAlchemy with the app
db.init_app(app)

# 4. Create database tables within the application context
# This is commented out to prevent it from running every time the app starts.
# with app.app_context():
#   db.create_all()

@app.route('/')
def home():
    sort_by = request.args.get('sort_by', 'title')
    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()

    book_list = []
    for book in books:
        book_info = {
            'title': book.title,
            'author': book.author.name,
            'cover_url': f"https://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg"
        }
        book_list.append(book_info)
    return render_template('home.html', books=book_list)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birth_date']
        
        birth_date = None
        if birth_date_str:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        new_author = Author(name=name, birth_date=birth_date)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('add_author'))
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author']

        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))
    
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)

if __name__ == '__main__':
    app.run(debug=True)
