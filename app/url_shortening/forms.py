from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import URL
from wtforms.validators import DataRequired


class CreateURLForm(Form):
    input_url = StringField(
            'Input URL',
            validators=[
                    URL(require_tld=True, message=u'Invalid URL.'),
                    DataRequired()])

    shorten_url = StringField('Shorten URL', validators=[URL()])
