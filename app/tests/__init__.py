import unittest
from app import app
from app import db


class TestBoilerPlate(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
