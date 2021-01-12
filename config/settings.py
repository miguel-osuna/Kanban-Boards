"""
Environment Configuration
"""

import os
from datetime import timedelta
from distutils.util import strtobool


class Config(object):
    """ Configuration base class. """

    # Flask Configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    SERVER_NAME = os.getenv("SERVER_NAME", None)

    # Celery Configuration
    CELERY_TASK_LIST = [
        "kanban_boards.blueprints.contact.tasks",
    ]
    CELERYBEAT_SCHEDULE = {}
    CELERY = {
        "broker_url": os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
        "result_backend": os.getenv(
            "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
        ),
        "accept_content": ["json"],
        "task_serializer": "json",
        "result_serializer": "json",
        "redis_max_connections": 5,
        "include": CELERY_TASK_LIST,
        "beat_schedule": CELERYBEAT_SCHEDULE,
    }

    # Flask Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = os.getenv("MAIL_PORT", 587)
    MAIL_USE_TLS = bool(strtobool(os.getenv("MAIL_USE_TLS", "true")))
    MAIL_USE_SSL = bool(strtobool(os.getenv("MAIL_USE_SSL", "false")))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = (
        "Tides",
        os.getenv("MAIL_DEFAULT_SENDER", "no-reply@email.com"),
    )

    # Flask-WTF Configuration
    RECAPTCHA_USER_SSL = bool(strtobool(os.getenv("RECAPTCHA_USER_SSL", "false")))
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", None)
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", None)
    RECAPTCHA_DATA_ATTRS = {"theme": "light", "size": "normal"}

    # Flask-Babel Configuration
    LANGUAGES = {"en": "English", "es": "Spanish"}
    BABEL_DEFAULT_LOCALE = "en"

    # Flask-Login Configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=90)

    # SQLAlchemy Configuration
    pg_user = os.getenv("POSTGRES_USER", "admin")
    pg_password = os.getenv("POSTGRES_PASSWORD", "password")
    pg_host = os.getenv("POSTGRES_HOST", "postgres")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    pg_db_name = os.getenv("POSTGRES_DB", "kanban_boards")
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        pg_user, pg_password, pg_host, pg_port, pg_db_name
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Seed Data Configuration
    SEED_ADMIN_USERNAME = os.getenv("SEED_ADMIN_USERNAME", "admin")
    SEED_ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "admin@email.com")
    SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "password")


class ProductionConfig(Config):
    """ Production environment configuration class. """

    # Flask Configuration
    ENV = "production"


class DevelopmentConfig(Config):
    """ Development environment configuration class. """

    # Flask Configuration
    ENV = "development"
    DEBUG = True

    # Werkzeug Configuration
    WERKZEUG_DEBUG_PIN = "off"


class TestingConfig(Config):
    """ Testing environment configuration class. """

    # Flask Configuration
    ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = "testing"

    # Werkzeug Configuration
    WERKZEUG_DEBUG_PIN = "off"

    # Flask-WTF Configuration
    WTF_CSRF_ENABLED = False

    # Flask-SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = "{0}_test".format(Config.SQLALCHEMY_DATABASE_URI)


# App configuration dictionary
app_config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
