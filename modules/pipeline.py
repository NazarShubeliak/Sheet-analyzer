from config.config import (
    API_URL,
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_SHEET_NAME,
    WORKSHEET_NAME,
)

from .loaders.currency_api import get_currency_ratest
from .loaders.sheet import SheetLoader


def run_pipeline() -> None:
    pass
