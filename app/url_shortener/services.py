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


def shorten_url(url_id):
    """Given an URL id return a shorten URL for it.
    We will simply convert the url_id which is an expected
    to be an unique decimal integer to a higher base(62)"""

    dictionary = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(dictionary)

    if url_id == 0:
        return url_id

    result = []
    while url_id:
        remainder = url_id % base
        url_id = url_id / base
        result.append(dictionary[remainder])

    return ''.join(result)


def create_url(original_url, user=None, short_url=None):
    """Creates the URL object and saves to the db."""

    if user is not None:
        url = URL(user=user, original_url=original_url)
    else:
        url = URL(original_url=original_url)

    # Insert the URL in the database so we have its id.
    db.session.add(url)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None

    # If no short_url generate one.
    if short_url:
        url.shorten_url = short_url
    else:
        url.shorten_url = shorten_url(url.id)

    # And now save to the database.
    db.session.add(url)
    db.session.commit()

    return url
