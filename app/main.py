# -*- coding: utf-8 -*-
from app import app

from url_shortener import views
from users import views as user_views
import errors as error_views

if __name__ == '__main__':
    app.run(debug=True)
