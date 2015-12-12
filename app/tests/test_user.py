# -*- coding: utf-8 -*-
"""Tests for the user module."""

import unittest

from users import models
from app import app
from app import db


def makeOne(**kwargs):
    """Creates an user and return its id"""

    default = {
        'username': 'abc',
        'password': 'abc'
    }

    default.update(kwargs)
    user = models.User(**default)
    return user


class TestUserModel(unittest.TestCase):
    """Test user models."""

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_create_user(self):
        user = makeOne()
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.id, 1)


class TestUserService(unittest.TestCase):
    """Test services provided by the user module."""

    def test_upper(self):
        self.assertTrue(True)


class TestUserView(unittest.TestCase):
    """Test user views."""

    def test_upper(self):
        self.assertTrue(True)
