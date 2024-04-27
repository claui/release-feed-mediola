"""A place for shared paths and settings."""

from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
PACKAGE_ROOT = Path(__file__).parent.absolute()
PYPROJECT_TOML = PROJECT_ROOT / 'pyproject.toml'

DOWNLOADS_JSON_URL = \
    'https://www.mediola.com/wp-content/sub-projects/helpdesk/data/downloads.json'
DOWNLOADS_WEB_URL_TEMPLATE = \
    'https://www.mediola.com/service#downloads?type=software&product={product_name}'
FEED_DESCRIPTION_TEMPLATE = 'Software releases for {product_name}'
FEED_LANGUAGE = 'de'
FEED_NAMESPACE = 'https://mediola.com/service/downloads'
FEED_SOURCE_LANGUAGE = 'de'
FEED_TITLE_TEMPLATE = '{product_name} – Releases'
MEDIOLA_IMPLIED_TIMEZONE = ZoneInfo('Europe/Berlin')

# List generated with Bash command line:
# curl -L "${DOWNLOADS_JSON_URL?}" | jq -cr '.de.software | keys'
MEDIOLA_PRODUCTS = [
    'aioremote', 'aioremote_desktop', 'configtool', 'configtoolneo',
    'firmware', 'iqontrol', 'iqontrol_neo', 'neo', 'neoserver',
    'neoserver_ccu3', 'qrcompanion', 'steckerpro'
]

REQUEST_TIMEOUT_SEC = 20
