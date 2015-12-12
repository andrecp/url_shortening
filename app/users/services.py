# -*- coding: utf-8 -*-
from app import db
from app import login_manager
from .models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


@login_manager.user_loader
def load_user(user_id):
    """Load an user from the database by an user_id, required
    by flask-login extension.
    """

    try:
        user = User.query.filter_by(id=int(user_id)).one()
    except NoResultFound:
        return None
    return user


def create_user(username, password):
    """Service to create a new user"""

    user = User(username=username, password=password)
    # Insert the user in the database
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return user


def lookup_user(username):
    """Lookup an user by username"""

    try:
        user = User.query.filter_by(username=username).one()
    except NoResultFound:
        return None
    return user


def password_matches(user, password):
    """Check if the password matches the user's."""

    return user.password == password
