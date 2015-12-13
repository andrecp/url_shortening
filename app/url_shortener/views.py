# -*- coding: utf-8 -*-

from flask import url_for, render_template, redirect, flash, abort
from flask.ext import login as flask_login

from app import app

from users import forms as users_forms
from . import forms as url_forms
from . import services


@app.route('/')
def index_view():
    """Home view."""

    signup_form = users_forms.SignUpForm()
    url_form = url_forms.CreateURLForm()
    return render_template('home.html',
                           signup_form=signup_form,
                           url_form=url_form)


@app.route('/shorten_url', methods=['GET', 'POST'])
def shorten_url_view():
    """Shorten the respective URL."""

    url_form = url_forms.CreateURLForm()
    if url_form.validate_on_submit():
        real_url = url_form.input_url.data
        short_url = url_form.shorten_url.data
        # If a shorten URL is given we look if it exists.
        if short_url:
            has_url = services.lookup_url_by_shorten(short_url)
            if has_url:
                flash('Short URL already registered')
                return render_template('create_url.html',
                                       url_form=url_form)
        else:
            short_url = services.shorten_url(real_url)
        # Check if we have an user.
        user = flask_login.current_user._get_current_object()
        if not user.is_authenticated:
            user = None
        # Create the URL, if the user exists redirect to its
        # profile, else go to a success page.
        url = services.create_url(real_url, short_url, user)
        if url:
            if user:
                return redirect(url_for('user_view', username=user.username))
            else:
                return render_template('success.html', url=real_url)

    return render_template('create_url.html',
                           url_form=url_form)


@app.route('/discover_url', methods=['GET', 'POST'])
def discover_url_view():
    """Return the real URL behind the shorten one."""

    url_form = url_forms.DiscoverURLForm()
    real_url = None
    if url_form.validate_on_submit():
        short_url = url_form.input_url.data
        real_url = services.lookup_url_by_shorten(short_url)
        if not real_url:
            flash('Short URL not registered')
        else:
            real_url = real_url.original_url
    return render_template('discover_url.html',
                           url_form=url_form,
                           real_url=real_url)


@app.route('/r/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    """Shorten the respective URL."""

    print short_url
    real_url = services.lookup_url_by_shorten(short_url, increment=True)
    if not real_url:
        abort(404)

    return redirect(real_url.original_url)
