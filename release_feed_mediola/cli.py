"""Entry point for the command line interface."""

import sys
from typing import NoReturn

from . import api
from .settings import MEDIOLA_PRODUCTS


def run(*args: str) -> NoReturn:
    """Runs the command line interface."""
    if not (combined_args := list(args) + sys.argv[1:]):
        print(
            f'Usage: {sys.argv[0]} [{" | ".join(MEDIOLA_PRODUCTS)}]',
            file=sys.stderr
        )
        sys.exit(1)
    print(api.release_feed(*combined_args[:1]))
    sys.exit(0)
