# -*- coding: utf-8 -*-

from datetime import datetime

from app import db


class URL(db.Model):
    """URL model"""

    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='urls')

    original_url = db.Column(db.String(80))
    shorten_url = db.Column(db.String(80), unique=True)

    clicks = db.Column(db.Integer())
    created = db.Column('c', db.DateTime, default=datetime.utcnow)
