import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Authors, Books, setup_db


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # Test database name
        self.database_name = "test"

        self.database_path = "postgresql://postgres:wafa@localhost:5432/"
        + self.database_name
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.reviewr = os.environ['reviewr']
            self.author = os.environ['author']
            self.reader = os.environ['reader']

        self.new_book = {
            'book_name': 'Structure and Interpretation of Computer Programs',
            'book_type': 'Coding Fundamentals',
            'book_rate': 4}

        self.new_auther = {
            'auth_name': 'Jon Stokes',
            'auth_gender': 'Male'}

        self.change_book = {
            'book_name': 'Structure and Interpretation of Computer Programs',
            'book_type': 'Coding Fundamentals',
            'book_rate': 7}

        self.change_auther = {
            'auth_name': 'Jon Stokes',
            'auth_gender': 'Male'}

        self.current_book_id = Books.query.order_by(Books.id.desc()).first().id
        self.current_auther_id = Authors.query.order_by(
            Authors.id.desc()).first().id

    def test_welcome_page(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_post_book_valid_token(self):
        res = self.client().post(
            '/books',
            headers={
                "Authorization": "Bearer {}".format(
                    self.reviewr)},
            json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_post_author_valid_token(self):
        res = self.client().post(
            '/authors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.reviewr)},
            json=self.new_auther)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_post_book_not_valid_token(self):
        res = self.client().post(
            '/books',
            headers={
                "Authorization": "Bearer {}".format(
                    self.reader)},
            json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_post_author_not_valid_token(self):
        res = self.client().post(
            '/authors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.reader)},
            json=self.new_auther)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_get_last_book(self):
        res = self.client().get('/last_book')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_last_auther_valid_token(self):
        res = self.client().get(
            '/last_author',
            headers={
                "Authorization": "Bearer {}".format(
                    self.reviewr)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_last_auther_not_valid_token(self):
        res = self.client().get(
            '/last_author',
            headers={
                "Authorization": "Bearer {}".format(
                    self.reader)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_book_by_id(self):
        res = self.client().get('/books/' + str(self.current_book_id),
                                headers={"Authorization": "Bearer {}"
                                .format(self.reader)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_patch_book_by_id(self):
        res = self.client().patch('/books/' + str(self.current_book_id),
                                  headers={"Authorization": "Bearer {}"
                                  .format(self.reviewr)},
                                  json=self.change_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_patch_book_by_id_not_valid_token(self):
        res = self.client().patch('/books/' + str(self.current_book_id),
                                  headers={"Authorization": "Bearer {}"
                                  .format(self.reader)},
                                  json=self.change_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_patch_auther_by_id(self):
        res = self.client().patch('/authors/' + str(self.current_auther_id),
                                  headers={"Authorization": "Bearer {}"
                                  .format(self.reviewr)},
                                  json=self.change_auther)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_patch_auther_by_id_not_valid_token(self):
        res = self.client().patch('/authors/' + str(self.current_auther_id),
                                  headers={"Authorization": "Bearer {}"
                                  .format(self.author)},
                                  json=self.change_auther)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_book_by_id(self):
        res = self.client().delete('/books/' + str(self.current_book_id),
                                   headers={"Authorization": "Bearer {}"
                                   .format(self.reviewr)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_delete_book_by_id_not_valid_token(self):
        res = self.client().delete('/books/' + str(self.current_book_id),
                                   headers={"Authorization": "Bearer {}"
                                   .format(self.reader)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_auther_by_id(self):
        res = self.client().delete('/authors/' + str(self.current_auther_id),
                                   headers={"Authorization": "Bearer {}"
                                   .format(self.reviewr)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_delete_auther_by_id_not_valid_token(self):
        res = self.client().delete('/authors/' + str(self.current_auther_id),
                                   headers={"Authorization": "Bearer {}"
                                   .format(self.author)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        """Executed after each test"""
        pass


if __name__ == "__main__":
    unittest.main()
