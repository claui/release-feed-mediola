"""
.. include:: ../README.md

## API Documentation
"""

# Re-export these symbols
# (This promotes them from release_feed_mediola.api to release_feed_mediola)
from release_feed_mediola.api import Api as Api

from release_feed_mediola.version import version

__all__ = [
    # Tell pdoc to pick up all re-exported symbols
    'Api',

    # Modules that every subpackage should see
    # (This also exposes them to pdoc)
    'api',
    'settings',
]

__version__ = version()
