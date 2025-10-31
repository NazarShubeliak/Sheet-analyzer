from typing import Dict

import requests

from config.config import logger


def get_currency_ratest(api_url: str) -> Dict[str, float]:
    """
    Fetch raw currency rates from external API.

    Args:
        api_url (str): Full API endpoint

    Returns:
        Dict[str, float]: Dictionary of currency -> rate to EUR

    Example response:
        {
            "data": {
                "CHF": 0.92,
                "CZK": 24.33,
                "PLN": 4.24
            }
        }
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        rates = response.json().get("data", {})
        logger.debug(f"Featched {len(rates)} currency rates from API")
        return {k.upper(): float(v) for k, v in rates.items()}
    except Exception as e:
        logger.error(f"Currency API error: {e}")
        raise
