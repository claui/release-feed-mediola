# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use, too-many-public-methods

from collections.abc import Callable
from datetime import datetime
import json
from typing import Any, cast

import pytest

from release_feed_mediola import feed


CURRENT = "current"


@pytest.fixture(autouse=True)
def disable_requests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove the attribute requests.sessions.Session.request.
    This is a safeguard against inadvertent network requests,
    causing them to fail."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture(name="neo_package")
def fixture_packages_by_name() -> dict[str, Any]:
    with open("tests/fixtures/neo.json", encoding="utf-8") as neo_json:
        filtered_dict = {
            version_key: release
            for version_key, release in json.load(neo_json).items()
            if version_key == CURRENT
        }
        return cast(dict[str, Any], filtered_dict)


@pytest.fixture(name="now")
def fixture_now() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat("2022-10-01T14:46:53+02:00")


def test_from_dict(neo_package: dict[str, Any], now: Callable[..., datetime]) -> None:
    expected = """<?xml version="1.0" encoding="utf-8"?>
<feed xml:lang="de" xmlns="http://www.w3.org/2005/Atom"><title>neo – Releases</title><link href="https://www.mediola.com/service#downloads?type=software&amp;product=neo" rel="alternate"></link><id>https://mediola.com/service/downloads</id><updated>2022-09-26T00:00:00+02:00</updated><subtitle>Software releases for neo</subtitle><entry><title>2.11.3</title><link href="https://www.mediola.com/service#downloads?type=software&amp;product=neo" rel="alternate"></link><published>2022-09-26T00:00:00+02:00</published><updated>2022-09-26T00:00:00+02:00</updated><id>https://mediola.com/service/downloads/versions/2.11.3</id><summary type="html">Version 2.11.3</summary><rights>https://www.mediola.com/eula</rights></entry></feed>"""  # pylint: disable=line-too-long
    assert feed.from_dict("neo", neo_package, now).strip() == expected
