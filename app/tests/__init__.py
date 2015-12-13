import unittest
from app import app
from app import db

# Import all the routes.
from url_shortener import views
from users import views as user_views
import errors as error_views


class TestBoilerPlate(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        self.db = db

    def tearDown(self):
        db.session.remove()
        db.drop_all()
