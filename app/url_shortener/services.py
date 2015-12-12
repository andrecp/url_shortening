# -*- coding: utf-8 -*-
from app import db
from app import login_manager
from .models import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


def lookup_url_by_shorten(url):
    """Lookup the URL given a shorten URL"""

    try:
        url = URL.query.filter_by(shorten_url=url).one()
    except NoResultFound:
        return None
    return url
