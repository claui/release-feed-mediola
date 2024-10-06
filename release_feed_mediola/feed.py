"""Generates a feed for a given Mediola product."""

from collections.abc import Callable
from datetime import date, datetime, time
from typing import Any

import feedgenerator  # type: ignore


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
    _now: Callable[..., datetime] = lambda: datetime.now(MEDIOLA_IMPLIED_TIMEZONE),
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
        Note: the current implementation no longer uses the current
        system time. The parameter is left for backwards
        compatibility.

    :return: the generated Atom feed as a string.
    """
    filtered_release_infos = (
        release[INFO] for _, release in releases_by_version.items() if INFO in release
    )
    context = {"product_name": product_name}
    feed = feedgenerator.Atom1Feed(
        id=FEED_NAMESPACE,
        title=FEED_TITLE_TEMPLATE.format(**context),
        link=DOWNLOADS_WEB_URL_TEMPLATE.format(**context),
        description=FEED_DESCRIPTION_TEMPLATE.format(**context),
        language=FEED_LANGUAGE,
    )
    for info in filtered_release_infos:
        feed.add_item(
            unique_id=f"{FEED_NAMESPACE}/versions/{info["version"]}",
            title=info["version"],
            description=f"Version {info["version"]}",
            link=DOWNLOADS_WEB_URL_TEMPLATE.format(**context),
            item_copyright=info["license"],
            pubdate=_datetime_from_iso_date(info.get("releasedate")),
            updateddate=_datetime_from_iso_date(info.get("releasedate")),
        )
    return str(feed.writeString(encoding="utf-8"))


def _datetime_from_iso_date(iso_date: str | None) -> datetime | None:
    if iso_date is None:
        return None
    _date = date.fromisoformat(iso_date)
    return datetime.combine(_date, time.min, tzinfo=MEDIOLA_IMPLIED_TIMEZONE)
