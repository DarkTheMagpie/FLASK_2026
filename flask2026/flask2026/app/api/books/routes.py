from flask import Blueprint, jsonify, request
from app.models import Book
from app.extensions import db

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

@books_bp.get("")
def get_books():
    books = Book.query.all()

    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "publication_year": book.publication_year,
            "description": book.description,
        })

    return jsonify(result)


@books_bp.post("")
def add_book():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Отправь JSON с данными книги"}), 400

    title = data.get("title")
    author = data.get("author")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Укажи название книги"}), 400

    if not isinstance(author, str) or not author.strip():
        return jsonify({"error": "Укажи автора книги"}), 400

    book = Book(
        title=title.strip(),
        author=author.strip(),
        publication_year=data.get("publication_year"),
        description=data.get("description"),
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({"id": book.id, "message": "Книга добавлена"}), 201
    

@books_bp.get("/<int:book_id>")
def get_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error": "Книга не найдена"}), 404

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "publication_year": book.publication_year,
        "description": book.description,
    })