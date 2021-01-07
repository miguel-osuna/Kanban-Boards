from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextAreaField
from wtforms_components import EmailField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    email = EmailField(
        "Waht's your e-mail address?", validators=[DataRequired(), Length(3, 254)]
    )
    message = TextAreaField(
        "What's your question or issue?", validators=[DataRequired(), Length(1, 8192)]
    )
    recaptcha = RecaptchaField()
