# -*- coding: utf-8 -*-
"""Tests for the url shortener module."""

import unittest

from url_shortener import services
from users import models as user_model
from url_shortener import models as url_model

from sqlalchemy.exc import IntegrityError
from .test_user import makeOne as makeUser
from app import app
from app import db


def makeOne(**kwargs):
    """Creates an url and return it"""

    default = {
        'original_url': 'original_url',
        'short_url': 'shorten_url'
    }

    default.update(kwargs)
    url = url_model.URL(**default)
    db.session.add(url)
    db.session.commit()
    return url


class TestURLShortenerModel(unittest.TestCase):
    """Test URL shortener models."""
    pass


class TestURLShortenerService(unittest.TestCase):
    """Test services provided by the URL shortener module."""

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_shorten_url(self):
        """shorten_url service should encode urls properly.. """

        shortner = services.shorten_url

        # Exercise with some known values.
        self.assertEquals(0, shortner(0))
        self.assertEquals('a', shortner(10))
        self.assertEquals('Yb8', shortner(31494))
        self.assertEquals('zOYKUa', shortner(9999999999))

    def test_lookup_url(self):
        """given a short url returns the URL object.. """

        lookup = services.lookup_url_by_shorten

        # We don't have any URLs...
        self.assertEquals(None, lookup('idontexist'))

        # Create one and it should exist.
        url = makeOne()
        self.assertEquals(url, lookup(url.short_url))

    def test_create_url(self):
        """given a short url returns the URL object.. """

        create_url = services.create_url

        # Let's create an URL object.
        url = create_url('http://www.google.com', user=None, short_url=None)
        # For the first 10 URLs the short_url matches the id.
        self.assertEquals(url.id, int(url.short_url))

        # Now let's create an URL passing a short url.
        url = create_url('http://www.google.com', user=None, short_url='xx')
        self.assertEquals(u'xx', url.short_url)

        # However, adding an already existing short url should raise an exc.
        self.assertRaises(IntegrityError, create_url, *['http://www.google.com', None, 'xx'])
        db.session.rollback()

        # Now let's do it with an user. It should have the url in its urls.
        user = makeUser()
        url = create_url('http://www.google.com', user=user, short_url='yy')
        self.assertIn(url, user.urls)


class TestURLShortenerView(unittest.TestCase):
    """Test URL shortener views."""

    pass
