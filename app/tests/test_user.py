# -*- coding: utf-8 -*-
"""Tests for the user module."""

import unittest

from users import models
from users import services
from app import db

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


class TestUserView(unittest.TestCase):
    """Test user views."""

    def test_upper(self):
        self.assertTrue(True)
