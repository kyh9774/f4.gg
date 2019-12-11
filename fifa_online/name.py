from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = f.StringField('구단주명', validators=[DataRequired()])
    display = ['name']

