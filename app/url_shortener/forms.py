from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import URL
from wtforms.validators import DataRequired
from wtforms.validators import Optional
from wtforms.validators import Length


class CreateURLForm(Form):
    input_url = StringField(
            'Input URL',
            validators=[
                    URL(require_tld=True, message=u'Invalid URL.'),
                    DataRequired()])

    short_url = StringField('Short URL', validators=[Optional(), Length(max=23)])


class DiscoverURLForm(Form):
    input_url = StringField(
            'Input URL',
            validators=[DataRequired()])
