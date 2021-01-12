from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_alchemy.validators import Unique
from wtforms_components import EmailField, Email

from config.settings import Config
from lib.util_wtforms import ModelForm, choices_from_dict
from kanban_boards.blueprints.user.models import User
from kanban_boards.blueprints.user.validations import (
    ensure_identity_exists,
    ensure_existing_password_matches,
)

LANGUAGES = Config.LANGUAGES


class SignupForm(ModelForm):
    username_message = "Letters, numbers and underscores only please."

    username = StringField(
        "Username",
        validators=[
            Unique(User.username),
            DataRequired(),
            Length(1, 16),
            Regexp(r"^\w+$", message=username_message),
        ],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Unique(User.email)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])


class LoginForm(FlaskForm):
    next = HiddenField()
    identity = StringField(
        "Username or email", validators=[DataRequired(), Length(3, 254)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me?")


class BeginPasswordResetForm(FlaskForm):
    identity = StringField(
        "Username or Email",
        validators=[DataRequired(), Length(3, 254), ensure_identity_exists],
    )


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])


class UpdateCredentialsForm(ModelForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired(), Length(8, 128), ensure_existing_password_matches],
    )

    email = EmailField(validators=[Email(), Unique(User.email)])
    password = PasswordField("New Password", [Optional(), Length(8, 128)])


class UpdateLocaleForm(FlaskForm):
    locale = SelectField(
        "Account language preference",
        validators=[DataRequired()],
        choices=choices_from_dict(LANGUAGES, prepend_blank=False),
    )


class AccountUnconfirmedForm(FlaskForm):
    pass
