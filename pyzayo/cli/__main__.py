"""
This file contains the zayocli main entrypoint for CLI purposes.  The `setup.py`
uses this file to install the CLI tool during package installation.

This file also servers to import each of the CLI components, which is why the
import modules list below exist.
"""
from .cli_root import cli

from . import cli_cases  # noqa
from . import cli_services  # noqa


def main():
    """ CLI main entrypoint """
    cli()
