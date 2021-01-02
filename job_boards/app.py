import os
from flask import Flask
from celery import Celery

from config.settings import app_config

CELERY_TASK_LIST = []


def create_celery_app(app=None):
    """ Create a new Celery instance and tie together the Celery config to the
    app's config. Wrap all tasks in the context of the application. 
    """
    app = app or create_app()

    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
        include=CELERY_TASK_LIST,
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(configuration="production"):
    """ Application factory, used to create an application. """

    # Create Flask application
    app = Flask("job_boards")

    # Setup app configuration from configuration object
    app.config.from_object(app_config[configuration])

    # Set logger level
    app.logger.setLevel(app.config["LOG_LEVEL"])

    @app.route("/")
    def index():
        return "Hello, World!"

    register_extensions(app)
    register_blueprints(app)
    register_error_templates(app)
    register_logger_exception_handler(app)
    register_shell_context(app)
    register_commands(app)

    return app


def register_extensions(app):
    return None


def register_blueprints(app):
    return None


def register_error_templates(app):
    return None


def register_logger_exception_handler(app):
    """ Flask will not send emails when Debug is set to True. """
    return None


def register_shell_context(app):
    return None


def register_commands(app):
    return None

