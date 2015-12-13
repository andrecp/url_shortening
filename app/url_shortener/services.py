# -*- coding: utf-8 -*-
from app import db
from .models import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


def lookup_url_by_shorten(url, increment=False):
    """Lookup the URL object given a shorten URL.
    If increment is set to True also increment the count.
    """

    try:
        url = URL.query.filter_by(shorten_url=url).one()
    except NoResultFound:
        return None
    if increment:
        url.clicks = url.clicks + 1
        db.session.add(url)
        db.session.commit()
    return url


def shorten_url(url):
    """Given an URL return a shorten version of it."""

    url = url.replace('.', '')
    if '://' in url:
        url = url.split('://')[-1]
    url = url.replace('/', '')

    return url


def create_url(original_url, shorten_url, user):
    """Creates the URL object and saves to the db."""

    if user is not None:
        url = URL(user=user, original_url=original_url, shorten_url=shorten_url)
    else:
        url = URL(original_url=original_url, shorten_url=shorten_url)

    # Insert the URL in the database
    db.session.add(url)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return url
