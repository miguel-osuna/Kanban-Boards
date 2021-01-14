from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _
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
    username_message = _("Letters, numbers and underscores only please.")

    username = StringField(
        _("Username"),
        validators=[
            Unique(User.username),
            DataRequired(),
            Length(1, 16),
            Regexp(r"^\w+$", message=username_message),
        ],
    )
    email = StringField(
        _("Email"), validators=[DataRequired(), Email(), Unique(User.email)]
    )
    password = PasswordField(_("Password"), validators=[DataRequired(), Length(8, 128)])


class LoginForm(FlaskForm):
    next = HiddenField()
    identity = StringField(
        _("Username or email"), validators=[DataRequired(), Length(3, 254)]
    )
    password = PasswordField(_("Password"), validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField(_("Remember me?"))


class BeginPasswordResetForm(FlaskForm):
    identity = StringField(
        _("Username or Email"),
        validators=[DataRequired(), Length(3, 254), ensure_identity_exists],
    )


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField(_("Password"), validators=[DataRequired(), Length(8, 128)])


class UpdateCredentialsForm(ModelForm):
    current_password = PasswordField(
        _("Current Password"),
        validators=[DataRequired(), Length(8, 128), ensure_existing_password_matches],
    )

    email = EmailField(validators=[Email(), Unique(User.email)])
    password = PasswordField(_("New Password"), [Optional(), Length(8, 128)])


class UpdateLocaleForm(FlaskForm):
    locale = SelectField(
        _("Account language preference"),
        validators=[DataRequired()],
        choices=choices_from_dict(LANGUAGES, prepend_blank=False),
    )


class AccountUnconfirmedForm(FlaskForm):
    pass
