# -*- coding: utf-8 -*-

from datetime import datetime

from app import db

from url_shortener.models import URL


class User(db.Model):
    """Users model
    Has some necessary boilerplate around flask-login and
    is storing password in an unsecure way.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    created = db.Column('c', db.DateTime, default=datetime.utcnow)
    modified = db.Column('m', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # XXX should be hashed.
    password = db.Column(db.String(80))

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
