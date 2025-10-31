from config.config import (
    API_URL,
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_SHEET_NAME,
    WORKSHEET_NAME,
    logger,
)

from .loaders.currency_api import get_currency_ratest
from .loaders.sheet import SheetLoader
from .processors.currency import normalize_to_eur
from .processors.dataframe import to_dataframe


def run_pipeline() -> None:
    # Step 1: Get data from Google Sheet
    sheet_loader = SheetLoader(GOOGLE_SHEET_NAME, GOOGLE_CREDENTIALS_PATH)
    sheet_loader.select_worksheet(WORKSHEET_NAME)
    data = sheet_loader.load_data()
    logger.info("Get data from Google Sheet")

    # Step 2: Get ratest from API
    rates = get_currency_ratest(API_URL)
    logger.info("Get ratest from API")

    # Step 3: Normalize currency to EUR
    data = normalize_to_eur(data, rates)
    logger.info("Normalize currency to EUR")

    # Step 4: Convert data to DataFrame structure
    logger.info("Convert data to DataFrame")
    return to_dataframe(data)
