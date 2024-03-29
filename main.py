from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://test_user:test_password@localhost:5432/test_db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    copies = db.relationship('Copy', backref='book', lazy=True)


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    patronymic = db.Column(db.String(255), nullable=True)
    copies = db.relationship('Copy', backref='reader', lazy=True)


class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), nullable=True)
    checkout_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)


@app.route('/create_book', methods=['POST'])
def create_book():
    data_title = request.form.get('title')
    data_author = request.form.get('author')
    print(data_author, data_title)
    new_book = Book(title=data_title, author=data_author)
    db.session.add(new_book)
    db.session.commit()
    new_copy = Copy(book_id=new_book.id)
    db.session.add(new_copy)
    db.session.commit()
    return redirect('/')


@app.route('/create_reader', methods=['POST'])
def create_reader():
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    patronymic = request.form.get('patronymic')
    new_reader = Reader(last_name=last_name, first_name=first_name, patronymic=patronymic)
    db.session.add(new_reader)
    db.session.commit()
    return redirect('/')


@app.route('/checkout_book', methods=['POST'])
def checkout_book():
    copy_id = request.form.get('copy_id')
    reader_id = request.form.get('reader_id')
    copy = Copy.query.get(copy_id)
    if copy and not copy.reader_id:
        copy.reader_id = reader_id
        copy.checkout_date = datetime.now()
        db.session.commit()
        return redirect('/')
    else:
        return {'error': 'Book not available'}


@app.route('/return_book', methods=['POST'])
def return_book():
    copy_id = request.form.get('copy_id')
    copy = Copy.query.get(copy_id)
    if copy and copy.reader_id:
        copy.reader_id = None
        copy.checkout_date = None
        copy.return_date = datetime.now()
        db.session.commit()
        return redirect('/')
    else:
        return {'error': 'Invalid copy or already returned'}


@app.route('/available_books', methods=['GET'])
def available_books():
    available_copies = Copy.query.filter_by(reader_id=None).all()
    books = [{'id': copy.id, 'title': copy.book.title, 'author': copy.book.author} for copy in available_copies]
    return render_template("books.html", some_books=books)


@app.route('/')
def main_page():
    return render_template("library.html")
