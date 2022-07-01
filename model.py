from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    search_bar = StringField('Movie Title', validators=[DataRequired()])
    search_button = SubmitField('Search')
