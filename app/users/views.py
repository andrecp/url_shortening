# -*- coding: utf-8 -*-
from app import app


@app.route('/signin', methods=['GET', 'POST'])
def signin_view():
    """Creates a new user."""
    return 'hi'


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    """Logs the user in."""
    return 'hi'


@app.route('/logout', methods=['POST'])
def logout_view():
    """Logs the user out."""
    return 'hi'


@app.route('/users/:username', methods=['GET'])
def users_id_view():
    """Lists the :username URLs."""
    return 'hi'
