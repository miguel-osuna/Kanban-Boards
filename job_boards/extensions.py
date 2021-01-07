""" Extensions module. Each extension is initialized in the app factory located in app.py. """

from celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_static_digest import FlaskStaticDigest

debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CSRFProtect()
# login_manager = LoginManager()
babel = Babel()
flask_static_digest = FlaskStaticDigest()
celery = Celery()
