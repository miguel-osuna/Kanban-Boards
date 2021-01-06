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
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    SERVER_NAME = os.getenv("SERVER_NAME")

    # Celery Configuration
    CELERY_TASK_LIST = []
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
    TESTING = True

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
