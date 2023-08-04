"""The primary module in release_feed_mediola."""

from collections.abc import Callable
from datetime import date, datetime, time
from typing import Any, cast

from feedgen.feed import FeedGenerator  # type: ignore
import requests

from .settings \
    import DOWNLOADS_JSON_URL, DOWNLOADS_WEB_URL_TEMPLATE, \
    FEED_DESCRIPTION_TEMPLATE, FEED_LANGUAGE, FEED_NAMESPACE, \
    FEED_SOURCE_LANGUAGE, FEED_TITLE_TEMPLATE, \
    MEDIOLA_IMPLIED_TIMEZONE, REQUEST_TIMEOUT_SEC

INFO = 'info'

def release_feed(product_name: str) -> str:
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

    if not product_name:
        raise ValueError('Name cannot be empty.')

    releases_by_version = _download_releases_by_version()
    packages_by_name = \
        releases_by_version[FEED_SOURCE_LANGUAGE]['software']
    if product_name not in packages_by_name:
        # List generated with:
        # curl -L $DOWNLOADS_JSON_URL | jq -cr '.de.software | keys'
        raise ValueError('Name must be one of:'
                         ' aioremote, aioremote_desktop, configtool,'
                         ' configtoolneo, firmware, iqontrol, iqontrol_neo,'
                         ' neo, neoserver, neoserver_ccu3, qrcompanion,'
                         ' steckerpro')
    return from_dict(product_name, packages_by_name[product_name])


def from_dict(product_name: str,
              releases_by_version: dict[str, Any],
              now: Callable[..., datetime] =
              lambda: datetime.now(MEDIOLA_IMPLIED_TIMEZONE)
              ) -> str:
    """Generates an Atom feed from a given releases-by-version
    dict.

    :param `product_name`:
        The feed title and description will refer to this name,
        and it will be used to link to a human-readable download
        page for the product.
        For a list of valid product names, see the `release_feed`
        function.

    :param `releases_by_version`:
        a dict of releases, whose values are a hierarchy of dicts
        where at least `info.version`, `info.license` and
        `info.releasedate` key paths.

    :param `now`:
        an optional supplier of the current system time in form of
        a `datetime`. If a supplier is given, it must return a
        `datetime` whose timezone is defined.

    :return: the generated Atom feed as a string.
    """
    filtered_release_infos = (
        release[INFO]
        for _, release in releases_by_version.items()
        if INFO in release
    )
    context = {
        'product_name': product_name
    }
    web_link = {
        'href': DOWNLOADS_WEB_URL_TEMPLATE.format(**context),
        'rel': 'alternate',
        'type': 'text/html',
    }
    generator = FeedGenerator()
    generator.id(FEED_NAMESPACE)
    generator.title(FEED_TITLE_TEMPLATE.format(**context))
    generator.language(FEED_LANGUAGE)
    generator.link(**web_link)
    generator.description(
        FEED_DESCRIPTION_TEMPLATE.format(**context))
    for info in filtered_release_infos:
        entry = generator.add_entry()
        entry.id(f'{FEED_NAMESPACE}/versions/{info["version"]}')
        entry.title(info['version'])
        entry.description(f'Version {info["version"]}')
        entry.link(**web_link)
        entry.rights(info['license'])
        entry.pubDate(_datetime_from_iso_date(info['releasedate']))
        entry.updated(_datetime_from_iso_date(info['releasedate']))
    generator.lastBuildDate(now())
    return str(generator.atom_str(pretty=True), encoding='utf-8')


def _download_releases_by_version() -> dict[str, Any]:
    response = requests.get(
        DOWNLOADS_JSON_URL, timeout=REQUEST_TIMEOUT_SEC)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


def _datetime_from_iso_date(iso_date: str) -> datetime:
    _date = date.fromisoformat(iso_date)
    return datetime.combine(
        _date, time.min, tzinfo=MEDIOLA_IMPLIED_TIMEZONE)
