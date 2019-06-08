"""
forms.py

Forms used in the Platform

"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """
    Login Form

    Used to Log In Students

    email(String, Email associated with account)
    password(String, Used for Verification)

    """
    username = StringField('Email', validators=[DataRequired()], render_kw={
        "placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
        "placeholder": "correcthorsebatterystaple"})
    submit = SubmitField('Submit')
