""" Extensions module. Each extension is initialized in the app factory located in app.py. """
import os

from celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_static_digest import FlaskStaticDigest
from flask_migrate import Migrate

MIGRATION_DIR = os.path.join("kanban_boards", "migrations")

debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
flask_static_digest = FlaskStaticDigest()
migrate = Migrate(directory=MIGRATION_DIR)
celery = Celery()
