# -*- coding: utf-8 -*-

from flask import render_template

from app import app

from users import forms as users_forms
from . import forms as url_forms


@app.route('/')
def index_view():
    """Home view."""

    signup_form = users_forms.SignUpForm()
    url_form = url_forms.CreateURLForm()
    return render_template('home.html',
                           signup_form=signup_form,
                           url_form=url_form)


@app.route('/shorten_url', methods=['POST'])
def shorten_url_view():
    """Shorten the respective URL."""

    return 'hello'
