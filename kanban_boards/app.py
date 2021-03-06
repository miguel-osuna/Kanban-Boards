import os
import logging
from logging.handlers import SMTPHandler

from flask import Flask, render_template, request
from flask_babel import _
from cli import register_cli_commands
from flask_login import current_user
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.proxy_fix import ProxyFix

from config.settings import app_config

# Blueprint imports
from kanban_boards.blueprints import page, contact, user, admin

# Extension imports
from kanban_boards.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    login_manager,
    babel,
    flask_static_digest,
    migrate,
    celery,
)

# Model imports
from kanban_boards.blueprints.user.models import User


def create_app(configuration="production"):
    """
    Application factory, used to create an application.

    :param configuration: Configuration dictionary
    :return: Flask app instance
    """

    # Create Flask application
    app = Flask("kanban_boards", static_folder="../public", static_url_path="")

    # Setup app configuration from configuration object
    app.config.from_object(app_config[configuration])

    # Set logger level
    app.logger.setLevel(app.config["LOG_LEVEL"])

    # Register utilities and dependencies
    middleware(app)
    register_extensions(app)
    register_blueprints(app)
    register_error_templates(app)
    register_template_processors(app)
    register_logger_exception_handler(app)
    # register_shell_context(app)
    register_commands(app)
    authentication(app, User)
    locale(app)
    init_celery(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


def register_extensions(app):
    """
    Register 0 or more flask extensions (mutates the app passed to it).

    :param app: Flask application instance
    :return: None
    """

    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    flask_static_digest.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """
    Register 0 or more blueprints (mutates the app passed to it).

    :param app: Flask application instance
    :return: None
    """

    app.register_blueprint(page)
    app.register_blueprint(contact)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    return None


def register_error_templates(app):
    """
    Register 0 or more error templates (mutates the app passed to it).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
        Render a custom templates for a specific

        :param status: Error status
        :type status: str
        :return: None
        """

        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, "code", 500)
        return render_template(f"errors/{code}.html"), code

    for error in [401, 404, 500]:
        app.errorhandler(error)(render_status)

    return None


def register_template_processors(app):
    """
    Register 0 or more template processors (mutates the app passed to it).

    :param app: Flask application instance
    :return: App jinja environment
    """
    return app.jinja_env


def register_logger_exception_handler(app):
    """
    Register 0 or more exception handlers (mutates the app passed to it).
    :

    :param app: Flask application instance
    :return: None
    """
    mail_handler = SMTPHandler(
        (app.config.get("MAIL_SERVER"), app.config.get("MAIL_PORT")),
        app.config.get("MAIL_USERNAME"),
        [app.config.get("MAIL_USERNAME")],
        "[Exception handler] A 5xx was thrown",
        (app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD")),
        secure=(),
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(
        logging.Formatter(
            """
        Time:               %(asctime)s
        Message type:       %(levelname)s

                
        Message:

        %(message)s
        """
        )
    )
    app.logger.addHandler(mail_handler)

    return None


def register_shell_context(app):
    """
    Registers shell context objects for the flask shell (mutates the app passed to it).

    :param app: Flask application instance
    :return: None
    """

    def shell_context():
        """ Shell context objects. """
        return dict(db=db, User=User)

    app.shell_context_processors(shell_context)
    return None


def register_commands(app):
    """
    Register 0 or more commands (mutates the app passed to it).

    :param app: Flask application instance
    :return: None
    """
    register_cli_commands(app)
    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swapp request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed to it).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_view = "user.login"
    login_manager.login_message = _("Please log in to access this page.")
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(user_id):
        user = user_model.query.get(user_id)

        if not user.is_active():
            login_manager.login_message = "This account has been disabled."
            login_manager.login_message_category = "error"
            return None

        return user


def locale(app):
    """
    Initialize a locale for the current request

    :param app: Flask application instance
    :return: str
    """
    if babel.locale_selector_func is None:

        @babel.localeselector
        def get_locale():
            if current_user.is_authenticated:
                return current_user.locale

            accept_languages = app.config.get("LANGUAGES").keys()
            return request.accept_languages.best_match(accept_languages)


def init_celery(app=None):
    """
    Configures a celery app and wraps all tasks in the context application.
    (mutates the app passed to it).

    :param app: Flask application instance
    :return: Celery instance

    """
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
