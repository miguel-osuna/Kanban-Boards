"""
Environment Configuration
"""

import os


class Config(object):
    """ Configuration base class. """

    # Flask Configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL")

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_REDIS_MAX_CONNECTIONS = 5

    # Flask Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # SQLAlchemy Configuration

    # Flask Login Configuration


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


# App configuration dictionary
app_config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
