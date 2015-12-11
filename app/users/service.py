# -*- coding: utf-8 -*-
import flask.ext.login as flask_login

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
