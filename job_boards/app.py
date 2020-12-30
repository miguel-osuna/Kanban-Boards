import os
from flask import Flask

from job_boards.settings import app_config


def create_app(configuration="production"):
    """ Application factory, used to create an application. """

    # Create Flask application
    app = Flask("job_boards")

    # Setup app configuration from configuration object
    app.config.from_object(app_config[configuration])

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)

    return app


def register_extensions(app):
    return None


def register_blueprints(app):
    return None


def register_error_handlers(app):
    return None


def register_shell_context(app):
    return None


def register_commands(app):
    return None

