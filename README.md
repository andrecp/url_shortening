[![Build Status](https://travis-ci.org/andrecp/url_shortening.svg?branch=master)](https://travis-ci.org/andrecp/url_shortening)

### Implementation of a URL shortening using Flask

#### Installing

Clone this repo and run ```pip install -r requirements.txt```.

Create the database by running ```python app/create_db.py```

#### Testing

Tests are localised under app/tests, you can run them by running ```nosetests app```.

They are currently ran automatically after every git push on Travis.

#### Running

If you have foreman installed you can run the WSGI app by running ```foreman start```. Else just run ```gunicorn --chdir app main:app -b localhost:5000```.

The WSGI app will be running in ```localhost:5000```.
