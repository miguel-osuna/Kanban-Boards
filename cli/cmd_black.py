import subprocess

import click

from flask.cli import with_appcontext


@click.command()
@click.argument("path", default=".")
@with_appcontext
def black(path):
    """
    Run python code formatter on the project.

    :param path: Project path
    :return: Subprocess call result
    """
    cmd = "black {0}".format(path)
    return subprocess.call(cmd, shell=True)
