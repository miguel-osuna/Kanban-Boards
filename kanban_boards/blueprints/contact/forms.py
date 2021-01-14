from flask_wtf import FlaskForm, RecaptchaField
from flask_babel import lazy_gettext as _
from wtforms import TextAreaField
from wtforms_components import EmailField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    email = EmailField(
        _("What's your e-mail address?"), validators=[DataRequired(), Length(3, 254)],
    )
    message = TextAreaField(
        _("What's your question or issue?"),
        validators=[DataRequired(), Length(1, 8192)],
    )
    recaptcha = RecaptchaField()
