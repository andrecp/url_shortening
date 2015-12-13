# -*- coding: utf-8 -*-
from flask import request, abort, redirect, url_for, render_template, flash
from flask.ext import login as flask_login
from app import app

from . import forms
from . import services


@app.route('/signup_login', methods=['GET', 'POST'])
def signup_login_view():
    """For the sake of simplicity we are using a single view
    for signup and login. We first try to log the user in,
    if it fails and the username is not taken we create it.
    """

    signup_form = forms.SignUpForm()
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        user = services.lookup_user(username)
        success = False
        if not user:
            user = services.create_user(username=username, password=password)
            if user:
                success = True
            else:
                flash('Invalid username or password')
        else:
            password_matches = services.password_matches(user, password)
            if password_matches:
                success = True
            else:
                flash('Wrong password')
        # If we either created the user or logged him in...
        if success:
            flask_login.login_user(user)
            flash('You were successfully logged in')
            return redirect(url_for('index_view'))

    return render_template('signup.html', signup_form=signup_form)


@app.route('/logout', methods=['POST'])
@flask_login.login_required
def logout_view():
    """Logs the user out."""

    flask_login.logout_user()
    return redirect(url_for('index_view'))


@app.route('/users/<username>', methods=['GET'])
@flask_login.login_required
def user_view(username):
    """Lists the :username URLs."""

    user = flask_login.current_user._get_current_object()
    if not user.username == username:
        abort(403)

    urls = user.urls

    return render_template('user.html', url_list=urls)
