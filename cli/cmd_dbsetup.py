import os
import subprocess

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy_utils import database_exists, create_database

from kanban_boards.extensions import db as db_ext
from kanban_boards.blueprints.user.models import User


@click.group()
def db():
    """ Run PostgreSQL related tasks. """
    pass


@db.command()
@click.option(
    "--with-testdb/--no-with-testdb", default=False, help="Create a test db too?"
)
@with_appcontext
def init(with_testdb):
    """
    Initialize the database

    :param with_testdb: Create a test database
    :return: None
    """

    # Drop the database and the recreates it with all the models
    db_ext.drop_all()
    db_ext.create_all()
    click.echo("Database created.")

    if with_testdb:
        db_uri = "{0}_test".format(current_app.config["SQLALCHEMY_DATABASE_URI"])

        if not database_exists(db_uri):
            create_database(db_uri)
            click.echo("Test database created.")

    return None


@db.command()
@with_appcontext
def seed():
    """
    Seed the databse with an initial user.

    :return: User instance
    """
    app_config = current_app.config

    # Make sure that the initial admin user doesn't exist
    if User.find_by_identity(app_config["SEED_ADMIN_EMAIL"]) is not None:
        return None

    params = {
        "role": "admin",
        "username": app_config["SEED_ADMIN_USERNAME"],
        "email": app_config["SEED_ADMIN_EMAIL"],
        "password": app_config["SEED_ADMIN_PASSWORD"],
        "confirmed": True,
    }

    click.echo("Seed user created.\n")
    return User(**params).save()


@db.command()
@click.option(
    "--with-testdb/--no-with-testdb", default=False, help="Create a test db too?"
)
@click.pass_context
@with_appcontext
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(seed)

    return None
