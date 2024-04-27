# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use, too-many-public-methods

from collections.abc import Callable
from datetime import datetime
import json
from typing import Any, cast

import pytest

from release_feed_mediola.api import Api


CURRENT = 'current'


@pytest.fixture(autouse=True)
def disable_requests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove the attribute requests.sessions.Session.request.
    This is a safeguard against inadvertent network requests,
    causing them to fail."""
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture(name='neo_package')
def fixture_packages_by_name() -> dict[str, Any]:
    with open('tests/fixtures/neo.json', encoding='utf-8') as neo_json:
        filtered_dict = {
            version_key: release
            for version_key, release in json.load(neo_json).items()
            if version_key == CURRENT
        }
        return cast(dict[str, Any], filtered_dict)


@pytest.fixture(name='now')
def fixture_now() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat('2022-10-01T14:46:53+02:00')


def test_from_dict(neo_package: dict[str, Any],
                   now: Callable[..., datetime]) -> None:
    expected = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de">
  <id>https://mediola.com/service/downloads</id>
  <title>neo – Releases</title>
  <updated>2022-10-01T14:46:53+02:00</updated>
  <link href="https://www.mediola.com/service#downloads?type=software&amp;product=neo" rel="alternate" type="text/html"/>
  <generator uri="https://lkiesow.github.io/python-feedgen" version="1.0.0">python-feedgen</generator>
  <subtitle>Software releases for neo</subtitle>
  <entry>
    <id>https://mediola.com/service/downloads/versions/2.11.3</id>
    <title>2.11.3</title>
    <updated>2022-09-26T00:00:00+02:00</updated>
    <content>Version 2.11.3</content>
    <link href="https://www.mediola.com/service#downloads?type=software&amp;product=neo"/>
    <published>2022-09-26T00:00:00+02:00</published>
    <rights>https://www.mediola.com/eula</rights>
  </entry>
</feed>
"""  # pylint: disable=line-too-long
    assert Api('neo').from_dict(neo_package, now) == expected
