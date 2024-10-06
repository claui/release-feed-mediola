"""The primary module in release_feed_mediola."""

from typing import Any, cast

import requests

from . import feed
from .logging import get_logger


from .settings import (
    DOWNLOADS_JSON_URL,
    FEED_SOURCE_LANGUAGE,
    MEDIOLA_PRODUCTS,
    REQUEST_TIMEOUT_SEC,
)


logger = get_logger(__name__)


class Api:  # pylint:disable=too-few-public-methods
    """Generates a release feed for the given package name.

    :param `product_name`:
        the product for which to generate a feed.
        Must be one of the values `aioremote`, `aioremote_desktop`,
        `configtool`, `configtoolneo`, `firmware`, `iqontrol`,
        `iqontrol_neo`, `neo`, `neoserver`, `neoserver_ccu3`,
        `qrcompanion` and `steckerpro`.

    :raises ValueError:
        if `product_name` is not one of the valid names.
    """

    def release_feed(
        self, product_name: str | None
    ) -> str:  # pylint: disable=no-self-use
        """Generates a release feed for the given package name.

        :param `product_name`:
            the product for which to generate a feed.
            Must be one of the values `aioremote`, `aioremote_desktop`,
            `configtool`, `configtoolneo`, `firmware`, `iqontrol`,
            `iqontrol_neo`, `neo`, `neoserver`, `neoserver_ccu3`,
            `qrcompanion` and `steckerpro`.

        :raises ValueError:
            if `product_name` is not one of the valid names.

        :return: a release feed for `product_name`.
        """

        releases_by_version = _download_releases_by_version()
        packages_by_name = releases_by_version[FEED_SOURCE_LANGUAGE]["software"]
        if not product_name:
            raise ValueError("Name cannot be empty.")
        if product_name not in packages_by_name:
            raise ValueError(
                f'Name must be one of: {", ".join(MEDIOLA_PRODUCTS)}',
            )
        return feed.from_dict(
            product_name,
            packages_by_name[product_name],
        )


def _download_releases_by_version() -> dict[str, Any]:
    response = requests.get(DOWNLOADS_JSON_URL, timeout=REQUEST_TIMEOUT_SEC)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())
