"""Generates a feed for a given Mediola product."""

from collections.abc import Callable
from datetime import date, datetime, time
from typing import Any

from feedgen.feed import FeedGenerator  # type: ignore


from .settings import (
    DOWNLOADS_WEB_URL_TEMPLATE,
    FEED_DESCRIPTION_TEMPLATE,
    FEED_LANGUAGE,
    FEED_NAMESPACE,
    FEED_TITLE_TEMPLATE,
    MEDIOLA_IMPLIED_TIMEZONE,
)

INFO = "info"


def from_dict(
    product_name: str,
    releases_by_version: dict[str, Any],
    now: Callable[..., datetime] = lambda: datetime.now(MEDIOLA_IMPLIED_TIMEZONE),
) -> str:
    """Generates an Atom feed from a given releases-by-version
    dict.

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
        release[INFO] for _, release in releases_by_version.items() if INFO in release
    )
    context = {"product_name": product_name}
    web_link = {
        "href": DOWNLOADS_WEB_URL_TEMPLATE.format(**context),
        "rel": "alternate",
        "type": "text/html",
    }
    generator = FeedGenerator()
    generator.id(FEED_NAMESPACE)
    generator.title(FEED_TITLE_TEMPLATE.format(**context))
    generator.language(FEED_LANGUAGE)
    generator.link(**web_link)
    generator.description(FEED_DESCRIPTION_TEMPLATE.format(**context))
    for info in filtered_release_infos:
        entry = generator.add_entry()
        entry.id(f'{FEED_NAMESPACE}/versions/{info["version"]}')
        entry.title(info["version"])
        entry.description(f'Version {info["version"]}')
        entry.link(**web_link)
        entry.rights(info["license"])
        entry.pubDate(_datetime_from_iso_date(info.get("releasedate")))
        entry.updated(_datetime_from_iso_date(info.get("releasedate")))
    generator.lastBuildDate(now())
    return str(generator.atom_str(pretty=True), encoding="utf-8")


def _datetime_from_iso_date(iso_date: str | None) -> datetime | None:
    if iso_date is None:
        return None
    _date = date.fromisoformat(iso_date)
    return datetime.combine(_date, time.min, tzinfo=MEDIOLA_IMPLIED_TIMEZONE)
