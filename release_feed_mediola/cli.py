"""Entry point for the command line interface."""

import os
import sys
from typing import NoReturn

import fire  # type: ignore

from . import __version__, api, fire_workarounds
from .errors import CliError
from .logging import get_logger
from .settings import MEDIOLA_PRODUCTS, PROJECT_ROOT, PYPROJECT_TOML


logger = get_logger(__name__)


def _version_text() -> str:
    if __version__ is None:
        return "release-feed-mediola (unknown version)"
    if os.path.exists(PYPROJECT_TOML):
        return (
            f"release-feed-mediola v{__version__}"
            + f" (in development at {PROJECT_ROOT})"
        )
    return f"release-feed-mediola v{__version__}"


def run(*args: str) -> NoReturn:
    # pylint: disable=magic-value-comparison
    """Runs the command line interface."""

    if not (combined_args := list(args) + sys.argv[1:]):
        print(
            f'Usage: {sys.argv[0]} [{" | ".join(MEDIOLA_PRODUCTS)}]',
            file=sys.stderr,
        )
        sys.exit(1)

    if sys.argv[1:] and sys.argv[1:][0] in {"-V", "--version"}:
        print(_version_text())
        sys.exit(0)

    fire_workarounds.apply()
    try:
        fire.Fire(api.Api, command=combined_args)
    except CliError as e:
        logger.error(e)
        sys.exit(1)
    sys.exit(0)
