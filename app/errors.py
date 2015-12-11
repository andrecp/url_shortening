# -*- coding: utf-8 -*-
"""Register error views."""

from flask import render_template
from app import app


@app.errorhandler(403)
def forbidden_view(e):
    return render_template('forbidden.html'), 403


@app.errorhandler(404)
def page_not_found_view(e):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def internal_error_view(e):
    return render_template('internal_error.html'), 500
