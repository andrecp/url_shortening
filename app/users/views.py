# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template
from flask.ext.login import login_user, logout_user
from app import app

from . import forms
from . import services


@app.route('/signup_login', methods=['GET', 'POST'])
def signup_login_view():
    """For the sake of simplicity we are using a single view
    for signup and login. We first try to log the user in,
    if it fails and the username is not taken we create it.
    """

    form = forms.SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = services.lookup_user(username)
        if not user:
            user = services.create_user(username=username, password=password)
        else:
            password_matches = services.password_matches(user, password)
        # If we either created the user or logged him in...
        if (user or password_matches):
            login_user(user)
            return redirect(url_for('index_view'))
    return render_template('home.html', signup_form=form)


@app.route('/logout', methods=['POST'])
def logout_view():
    """Logs the user out."""

    logout_user()
    return redirect(url_for('index_view'))


@app.route('/users/<username>', methods=['GET'])
def user_view(username):
    """Lists the :username URLs."""

    return render_template('user.html', url_list='url_list')
