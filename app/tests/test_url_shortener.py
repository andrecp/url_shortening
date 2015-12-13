# -*- coding: utf-8 -*-
"""Tests for the url shortener module."""

from url_shortener import services
from url_shortener import models as url_model
from test_user import makeOne as makeUser

from sqlalchemy.exc import IntegrityError
from app import db

from . import TestBoilerPlate


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


class TestURLShortenerModel(TestBoilerPlate):
    """Test URL shortener models."""

    def test_create_url(self):
        """Creating an URL should work..."""

        url = makeOne()
        self.assertTrue(url.id >= 1)

        # Two URLs with same shortcode should error.
        self.assertRaises(IntegrityError, makeOne)


class TestURLShortenerService(TestBoilerPlate):
    """Test services provided by the URL shortener module."""

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


class TestURLShortenerView(TestBoilerPlate):
    """Test URL shortener views."""

    def test_get_index(self):
        """Getting index should return 200..."""

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_redirect_to_url(self):
        """Should be able to redirect to an url from a short url..."""

        # Not yet created should 404.
        response = self.app.get('/r/1')
        self.assertEqual(response.status_code, 404)

        # Should redirect to the original URL and increment clicks.
        url = makeOne(**{'short_url': '1', 'original_url': 'http://www.google.com'})
        self.assertEqual(0, url.clicks)
        response = self.app.get('/r/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['location'], 'http://www.google.com')
        # Get again from the DB, should've one click.
        url = url_model.URL.query.filter_by(id=url.id).one()
        self.assertEqual(1, url.clicks)

    def test_get_discover_url(self):
        """Should be able to discover an url from a short url..."""

        # Not yet created...
        response = self.app.post('/discover_url', data={'input_url': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Short URL not registered' in response.data)
        # Creating...
        _ = makeOne(**{'short_url': '1', 'original_url': 'http://www.google.com'})
        response = self.app.post('/discover_url', data={'input_url': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('http://www.google.com' in response.data)
