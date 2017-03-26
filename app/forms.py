from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class DownloaderForm(Form):
    url_to_down = StringField('url', validators=[DataRequired()])
