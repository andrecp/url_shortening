from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Length
from wtforms.validators import URL
from wtforms.validators import DataRequired


class CreateURLForm(Form):
    input_url = StringField(
            'Input URL',
            validators=[
                    URL(require_tld=True, message=u'Invalid URL.'),
                    DataRequired(),
                    Length(max=23)])

    shorten_url = StringField('Shorten URL', validators=[URL()])


class DiscoverURLForm(Form):
    input_url = StringField(
            'Input URL',
            validators=[
                    URL(require_tld=True, message=u'Invalid URL.'),
                    DataRequired(),
                    Length(max=23)])
