# -*- coding: utf-8 -*-

from flask import render_template, redirect, flash

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

    return 'hello'


@app.route('/discover_url', methods=['GET', 'POST'])
def discover_url_view():
    """Return the real URL behind the shorten one."""

    url_form = url_forms.DiscoverURLForm()
    real_url = None
    if url_form.validate_on_submit():
        short_url = url_form.input_url.data
        real_url = services.lookup_url_by_shorten(short_url)
        if not real_url:
            flash('Short URL not registerd')
    return render_template('discover_url.html',
                           url_form=url_form,
                           real_url=real_url)
