from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from data_models import db, Author, Book
from datetime import datetime

# 1. Initialize the Flask app
app = Flask(__name__)

# 2. Configure the database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to suppress a warning

# 3. Initialize SQLAlchemy with the app
db.init_app(app)

# 4. Create database tables within the application context
with app.app_context():
  db.create_all()

@app.route('/')
def home():
    query = request.args.get('q')
    sort_by = request.args.get('sort_by', 'title')

    if query:
        books = Book.query.filter(Book.title.like(f"%{query}%"))
    else:
        books = Book.query

    if sort_by == 'author':
        books = books.join(Author).order_by(Author.name).all()
    else:
        books = books.order_by(Book.title).all()

    book_list = []
    for book in books:
        book_info = {
            'id': book.id,
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
        return redirect(url_for('add_book', author_id=new_author.id))
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
        return redirect(url_for('home'))
    
    authors = Author.query.all()
    selected_author_id = request.args.get('author_id', type=int)
    return render_template('add_book.html', authors=authors, selected_author_id=selected_author_id)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author
    db.session.delete(book)
    db.session.flush()

    if not author.books:
        db.session.delete(author)
        
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    author_name = author.name
    
    for book in author.books:
        db.session.delete(book)
        
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)