import os
from flask import Flask

from config.settings import app_config
from job_boards.extensions import celery


def create_app(configuration="production"):
    """ Application factory, used to create an application. """

    # Create Flask application
    app = Flask("job_boards", static_folder="../public", static_url_path="")

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
    init_celery(app)

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


def init_celery(app=None):
    """ Configures a celery app and wraps all tasks in the context application. """
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """ Make celery tasks work with Flask app context. """

        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
