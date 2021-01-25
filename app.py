import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Authors, Books, setup_db

from auth.auth import requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def greeting():
        return "Welcome"

    @app.route('/last_book')
    def get_books_info():
        try:
            data = []

            info = Books.query.all()
            for book in info:
                data.append({"book_name": book.book_name,
                             "book_type": book.book_type,
                             "book_rate": book.book_rate})
                return jsonify({
                    "success": True,
                    "books": data
                })

            book_info = [books.format() for book in info]

        except BaseException:
            abort(404)

        return jsonify({
            "success": True,
            "book": [info.format() for book in info]
        }), 200

    @app.route('/books/<int:id>')
    @requires_auth('get:books')
    def get_book_by_id(payload, id):
        try:
            info = Books.query.filter(Books.id == id).one_or_none()

        except BaseException:
            abort(401)

        return jsonify({
            "success": True,
            "book_name": info.book_name,
            "book_type": info.book_type,
            "book_rate": info.book_rate

        }), 200

    @app.route('/books', methods=['POST'])
    @requires_auth('post:books')
    def post_books(payload):
        body = request.get_json()
        try:

            book = Books(
                body['book_name'],
                body['book_type'],
                body['book_rate'])
            book.insert()

        except BaseException:
            abort(401)

        return jsonify({
            "sucess": True,
            "book": book.id

        }), 200

    @app.route('/books/<int:id>', methods=['DELETE'])
    @requires_auth('delete:books')
    def delete_books(payload, id):

        book = Books.query.filter(Books.id == id).one_or_none()
        if not book:
            abort(404)
        try:
            book.delete()
        except BaseException:
            abort(401)
        return jsonify({
            "sucess": True,
            "delete": id
        }), 200

    @app.route('/books/<int:id>', methods=['PATCH'])
    @requires_auth('patch:books')
    def patch_books(payload, id):

        book = Books.query.filter(Books.id == id).one_or_none()
        if not book:
            abort(404)
        try:
            book.update()
        except BaseException:
            abort(401)
        return jsonify({
            "sucess": True,
            "update": id
        }), 200

    @app.route('/last_author')
    @requires_auth('get:authors')
    def authors_info(payload):
        try:

            data = []

            info = Authors.query.all()
            for auth in info:
                data.append({"auth_name": auth.auth_name,
                             "auth_gender": auth.auth_gender
                             })
                return jsonify({
                    "success": True,
                    "author": data
                })
            author_info = [Authors.format() for auth in info]
        except BaseException:
            abort(401)

        return jsonify({
            "success": True,
            "authors": author_info
        }), 200

    @app.route('/authors', methods=['POST'])
    @requires_auth('post:authors')
    def post_authors(payload):

        body = request.get_json()

        author = Authors(
            body['auth_name'],
            body['auth_gender']

        )
        author.insert()

        return jsonify({
            "sucess": True,
            "auth_id": author.id
        }), 200

    @app.route('/authors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:authors')
    def delete_authors(payload, id):
        auth = Authors.query.filter(Authors.id == id).one_or_none()
        if not auth:
            abort(404)
        try:
            auth.delete()
        except BaseException:
            abort(403)
        return jsonify({
            "sucess": True,
            "delete": id
        }), 200

    @app.route('/authors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:authors')
    def patch_authors(payload, id):
        auth = Authors.query.filter(Authors.id == id).one_or_none()
        if not auth:
            abort(404)
        try:
            auth.update()
        except BaseException:
            abort(401)
        return jsonify({
            "sucess": True,
            "update": id
        }), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": error.__dict__
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.__dict__
        }), 401

    @app.errorhandler(400)
    def BadRequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(403)
    def BadRequest(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": 'Forbidden'
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
