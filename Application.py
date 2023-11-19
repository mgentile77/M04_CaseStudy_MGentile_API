from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
# app.app_context().push()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.VARCHAR(250), unique=True, nullable=False)
    author = db.Column(db.VARCHAR(80))
    publisher = db.Column(db.VARCHAR(80))

    def __repr__(self):
        return f"""\n{self.book_name}\n{self.author}\n{self.publisher}\n"""
    
    def to_dict(self):
        return {column.key: getattr(self, column.key) if not isinstance(getattr(self, column.key), db.Model) else None for column in class_mapper(self.__class__).mapped_table.c}

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Books.query.all()
    output = []
    for book in books:
        book_data = {'Book': book.book_name, 'Author': book.author, 'Publisher': book.publisher}
        output.append(book_data)
    return jsonify({'Books': output})

@app.route('/books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {'Book':book.book_name, 'Author':book.author, 'Publisher':book.publisher}

@app.route('/books',methods=['POST'])
def add_book():
    book = Books(book_name=request.json['book'],author=request.json['author'],publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>',methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return {'error': "not found"}
    db.session.delete(book)
    db.session.commit()
    return "Delete successful!"
    
    
    
if __name__ == '__main__':
    app.run(debug=True)