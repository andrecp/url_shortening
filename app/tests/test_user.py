# -*- coding: utf-8 -*-
"""Tests for the user module."""

import unittest

from users import models
from users import services
from app import db

from flask.ext import login as flask_login

from sqlalchemy.exc import IntegrityError

from . import TestBoilerPlate


def makeOne(**kwargs):
    """Creates an user and return it"""

    default = {
        'username': 'abc',
        'password': 'abc'
    }

    default.update(kwargs)
    user = models.User(**default)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserModel(TestBoilerPlate):
    """Test user models."""

    def test_create_user(self):
        """Creating an user should work..."""

        user = makeOne()
        self.assertTrue(user.id >= 1)
        # Two Users with same username should error.
        self.assertRaises(IntegrityError, makeOne)


class TestUserService(TestBoilerPlate):
    """Test services provided by the user module."""

    def test_load_user(self):
        """Loading an user from the db should work (Flask-Login)..."""

        load_user = services.load_user

        user = makeOne()
        user_id = user.id
        self.assertEqual(user, load_user(unicode(user_id)))

        # A non existing user should return None.
        self.assertEqual(None, load_user(unicode(50)))

    def test_create_user(self):
        """Creating an user should work just fine..."""

        create_user = services.create_user

        user = create_user('andre', 'test')
        self.assertTrue(user.id)

        # A second user with same username should return None
        user = create_user('andre', 'test')
        self.assertIsNone(user)

    def test_lookup_user(self):
        """Looking up an user by username should work..."""

        lookup_user = services.lookup_user

        user = makeOne()
        username = user.username
        self.assertEqual(user, lookup_user(unicode(username)))

        # A non existing user should return None.
        self.assertEqual(None, lookup_user(unicode('Idontexist')))

    def test_password_matches(self):
        """User password should match..."""

        password_matches = services.password_matches

        user = makeOne()
        password = user.password
        self.assertTrue(password_matches(user, password))
        self.assertFalse(password_matches(user, reversed(password)))


class TestUserView(TestBoilerPlate):
    """Test user views."""

    def test_signup_login_view(self):
        """An user should be able to login or create an user..."""

        # Just make sure it's there.
        response = self.app.get('/signup_login')
        self.assertEqual(response.status_code, 200)

        # Creating a new user.
        with self.app:
            total_users = len(models.User.query.all())
            response = self.app.post('/signup_login',
                                     data={'username': 'andre',
                                           'password': 'test'})
            self.assertEqual(response.status_code, 302)
            create_user = models.User.query.filter_by(username='andre').one()
            self.assertEqual(create_user.password, 'test')
            self.assertEqual(flask_login.current_user.username, 'andre')
            self.assertEqual(total_users + 1, len(models.User.query.all()))

        # Logging in doesn't create a new user.
        total_users = len(models.User.query.all())
        response = self.app.post('/signup_login', data={'username': 'andre', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(total_users, len(models.User.query.all()))

        # Wrong password.
        response = self.app.post('/signup_login', data={'username': 'andre', 'password': 'test1'})
        self.assertTrue('Wrong password' in response.data)
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """An user should be able to log out..."""

        # Have to be logged in to log out.
        response = self.app.post('/logout')
        self.assertEqual(response.headers['location'],
                         'http://localhost/signup_login?next=%2Flogout')
        self.assertEqual(response.status_code, 302)

        with self.app:
            _ = self.app.post('/signup_login',
                              data={'username': 'andre',
                                    'password': 'test'})
            self.assertEqual(flask_login.current_user.is_authenticated, True)
            _ = self.app.post('/logout')
            self.assertEqual(flask_login.current_user.is_authenticated, False)

    def test_user_listing_view(self):
        """An user should be able to see his urls..."""

        with self.app:
            _ = self.app.post('/signup_login',
                              data={'username': 'andre',
                                    'password': 'test'})
            response = self.app.get('/users/andre')
            self.assertEqual(response.status_code, 200)
            # Shouldn't be able to see other person's.
            response = self.app.get('/users/otherperson')
            self.assertEqual(response.status_code, 403)
