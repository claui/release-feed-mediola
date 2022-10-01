"""Entry point for the command line interface."""

import sys

from . import api


def run(*args: str) -> None:
    """Runs the command line interface."""
    combined_args = list(args) + sys.argv[1:]
    print(api.release_feed(*combined_args[:1]))
