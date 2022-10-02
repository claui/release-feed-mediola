"""Entry point for the command line interface."""

import sys
from typing import NoReturn

from . import api


def run(*args: str) -> NoReturn:
    """Runs the command line interface."""
    if not (combined_args := list(args) + sys.argv[1:]):
        print(f'Usage: {sys.argv[0]} [product_name]',
              file=sys.stderr)
        sys.exit(1)
    print(api.release_feed(*combined_args[:1]))
    sys.exit(0)
