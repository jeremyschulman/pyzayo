# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from importlib import metadata
from os import environ

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

import pyzayo
from pyzayo.consts import Env


# -----------------------------------------------------------------------------
# Module Exports
# -----------------------------------------------------------------------------

__all__ = ["cli"]

VERSION = metadata.version(pyzayo.__package__)


@click.group(invoke_without_command=True)
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx: click.Context):
    """
    Zayo CLI tool to access information via the API.
    """
    try:
        # Ensure the necessary environment variables are set before proceeding.
        all(environ[env_var] for env_var in Env.values())

    except KeyError as exc:
        ctx.fail(f"Missing environment variable: {exc}")
