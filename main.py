from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test_user:test_password@localhost:3306/test_db,'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


<<<<<<< HEAD
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
=======
class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    patronymic = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
>>>>>>> 3865874beb65c00a902909e2852ac4316af1e994


# main page
@app.route('/create_book', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'})


# Роут для создания нового читателя
@app.route('/create_reader', methods=['POST'])
def create_reader():
    data = request.get_json()
    new_reader = Reader(last_name=data['last_name'], first_name=data['first_name'], patronymic=data['patronymic'])
    db.session.add(new_reader)
    db.session.commit()
    return jsonify({'message': 'Reader created successfully'})


# Роут для выдачи книги читателю
@app.route('/checkout_book', methods=['POST'])
def checkout_book():
    data = request.get_json()
    copy_id = data['copy_id']
    reader_id = data['reader_id']
    copy = Copy.query.get(copy_id)
    if copy and not copy.reader_id:
        copy.reader_id = reader_id
        copy.checkout_date = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Book checked out successfully'})
    else:
        return jsonify({'error': 'Book not available'})


# Роут для возврата книги читателем
@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.get_json()
    copy_id = data['copy_id']
    copy = Copy.query.get(copy_id)
    if copy and copy.reader_id:
        copy.reader_id = None
        copy.checkout_date = None
        copy.return_date = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'})
    else:
        return jsonify({'error': 'Invalid copy or already returned'})


# Роут для получения списка доступных книг
@app.route('/available_books', methods=['GET'])
def available_books():
    available_copies = Copy.query.filter_by(reader_id=None).all()
    books = [{'id': copy.id, 'title': copy.book.title, 'author': copy.book.author} for copy in available_copies]
    return jsonify(books)


def main_page():
    return render_template("templates/library.html")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
