from flask import session
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, InputRequired


class AuthForm(FlaskForm):
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Zugriff!')


class SearchForm(FlaskForm):
    query = StringField('Suchbegriff', validators=[InputRequired()])
    submit = SubmitField('Download')


def get_password(share_id):
    if share_id not in session:
        return None
    else:
        return session[share_id]


def set_password(share_id, password):
    session[share_id] = password
    return password
