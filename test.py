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

        self.database_path = "postgresql://postgres:wafa@localhost:5432/" + self.database_name
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.reviewr = os.environ['reviewr']='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1jS2lkajJURE5vT3NzZDhnazVTUSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtd2FmYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwZTkwYTczYjJkMzQwMDY5ZDA3NzcwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTE1NjczMzQsImV4cCI6MTYxMTY1MzczNCwiYXpwIjoibTByVHlZYkF5UTB0Nm1yUks2N1JtbTIxSkxCV3B3ZnkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3JzIiwiZGVsZXRlOmJvb2tzIiwiZ2V0OmF1dGhvcnMiLCJnZXQ6Ym9va3MiLCJwYXRjaDphdXRob3JzIiwicGF0Y2g6Ym9va3MiLCJwb3N0OmF1dGhvcnMiLCJwb3N0OmJvb2tzIl19.rBiyzzat7R4IdHar_lx3gOgs7CxAG_zw21mMlYBCAa-SVehkKm3tp3k-CvRDWw3y7QMpnl9uKog-ZO0ADihWJfTKoKWUj_ikuDeTgQlkXjAbgfX84lreQwsqMWejsef23jNyvLjbosQU4v2tk4iyqrKg9np8vRUDKEtOLcFbl9auvsLqKdop9v3Fnhu4RjPUNmJK8fNWgaInT_3Yo_Rh4ogdODL0R41Wc02lt0BW2GdQd1E3OW-W5-nqpYdj2inbA5_vrKYFT_D44AQzY96m2DMJXParappTQ1PfpprwtEzvum6hu4hvx4GgAQRRFgnA_NJ7lbB3X4cZ3wmkzIik1Q'
            self.author = os.environ['author']='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1jS2lkajJURE5vT3NzZDhnazVTUSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtd2FmYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwZTk1MmYzYjJkMzQwMDY5ZDA3Nzk0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTE1Njg1OTQsImV4cCI6MTYxMTY1NDk5NCwiYXpwIjoibTByVHlZYkF5UTB0Nm1yUks2N1JtbTIxSkxCV3B3ZnkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicG9zdDpib29rcyJdfQ.fkg14431xjnLyE1xlOiFqeX7Gn6rLw2Y9FkFpdCAh1wvmvBkmi45v9B0wNAq0QUUimPjnkSY1Ni9YSfzGS_lvaly1Y8VtuJ7RIXWI4mVxOLsqO5tPlwJVhEA2GRbxznLHeN8K66FgEGm-Iu4QEu88gUJ_9GEN_i7oKpGzR0CDBU5vFocFa1HJ_11K1vgv_z8KoA4qPmb37RDx9NwxiIKvuAS4RluuhO9qoMjm7F3Y0FgG1HPdWHP4SnzPNOS7NIrLbXbLAohwQwnNSRMz8wq6cnGhVyDZzclZtKOxIknOj5yijANAiBBbfccyzYdF9BayHhysRU-35RMpe7IMnaGwg'
            self.reader = os.environ['reader']='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1jS2lkajJURE5vT3NzZDhnazVTUSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtd2FmYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwZTk2N2YzYjJkMzQwMDY5ZDA3N2IwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTE1Njg4MzcsImV4cCI6MTYxMTY1NTIzNywiYXpwIjoibTByVHlZYkF5UTB0Nm1yUks2N1JtbTIxSkxCV3B3ZnkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIl19.fmWvf8M8aBSZ5L6hPbn9yMG-oCudb1TtAW9nt4keUTN4edXvl0Ptugd_jzT89Pq-Ny_jmB2izc6M_T1GTh8mlnIaIewAHGZmHl6_MPJQY1j8L-szyZiUb4MGuh9YeKRYYnltwdKuG9tkAigvwXDw7AXIlrgvHRIApxLleHWpAub-sWFKgLh4pZkdFY6b4uP2xA_k8k-P9uQbQXeGMi5DpRh4miWBXlvIX4-HPoXExZvUUDM6Yby-AekU1Cz5ZwHrm-j7Q04tNvE3itgd36I04mM2PEKABajI-Up2FVetTK49vd1N8kF89M4kXIrTR_2nglaF5co6ocKBVYrxf-1TFA'

        
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
                                headers={"Authorization": "Bearer {}".format(self.reader)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

   

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_patch_book_by_id(self):
        res = self.client().patch('/books/' + str(self.current_book_id),
                                  headers={"Authorization": "Bearer {}".format(self.reviewr)},
                                  json=self.change_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_patch_book_by_id_not_valid_token(self):
        res = self.client().patch('/books/' + str(self.current_book_id),
                                  headers={"Authorization": "Bearer {}".format(self.reader)},
                                  json=self.change_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_patch_auther_by_id(self):
        res = self.client().patch('/authors/' + str(self.current_auther_id),
                                  headers={"Authorization": "Bearer {}".format(self.reviewr)},
                                  json=self.change_auther)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_patch_auther_by_id_not_valid_token(self):
        res = self.client().patch('/authors/' + str(self.current_auther_id),
                                  headers={"Authorization": "Bearer {}".format(self.author)},
                                  json=self.change_auther)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_book_by_id(self):
        res = self.client().delete('/books/' + str(self.current_book_id),
                                   headers={"Authorization": "Bearer {}".format(self.reviewr)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_delete_book_by_id_not_valid_token(self):
        res = self.client().delete('/books/' + str(self.current_book_id),
                                   headers={"Authorization": "Bearer {}".format(self.reader)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_auther_by_id(self):
        res = self.client().delete('/authors/' + str(self.current_auther_id),
                                   headers={"Authorization": "Bearer {}".format(self.reviewr)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_delete_auther_by_id_not_valid_token(self):
        res = self.client().delete('/authors/' + str(self.current_auther_id),
                                   headers={"Authorization": "Bearer {}".format(self.author)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        """Executed after each test"""
        pass


if __name__ == "__main__":
    unittest.main()
