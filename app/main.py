# -*- coding: utf-8 -*-
from app import app

from url_shortening import views
from users import views

if __name__ == '__main__':
    app.run(debug=True)
