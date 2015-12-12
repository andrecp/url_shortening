# -*- coding: utf-8 -*-
from app import db
from app import login_manager
from .models import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


def lookup_url_by_shorten(url):
    """Lookup the URL given a shorten URL."""

    try:
        url = URL.query.filter_by(shorten_url=url).one()
    except NoResultFound:
        return None
    return url


def shorten_url(url):
    """Given an URL return a shorten version of it."""

    return url


def create_url(user, original_url, shorten_url):
    """Creates the URL object and saves to the db."""

    url = URL(user=user, original_url=original_url, shorten_url=shorten_url)
    # Insert the URL in the database
    db.session.add(url)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return url
