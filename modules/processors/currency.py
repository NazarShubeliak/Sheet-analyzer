from typing import Dict, List

from config.config import logger


def normalize_to_eur(
    data: List[Dict[str, str]], rates: Dict[str, float]
) -> List[Dict[str, str]]:
    """
    Normalize 'Total' filed to EUR using provided exchange rates.

    Args:
        data (List[Dict[str, str]]): Raw data from Google Sheet
        rates (Dict[str, str]): Currency -> rate to EUR

    Returns:
        List[Dict[str, str]]: Data with added 'Total_EUR' filed

    Raises:
        ValueError: If unknown currency is encountered
    """
    normalize: List[Dict[str, float]] = []
    for row in data:
        try:
            amount = float(row.get("Total", 0))
            currency = row.get("Currency", "").upper()

            if currency in rates:
                rate = rates[currency]
                row["Total"] = round(amount / rate, 2)
            elif currency == "EUR":
                row["Total"] = round(amount, 2)
            else:
                message = f"Unknow currency '{currency}' encountered in row: {row}"
                logger.error(message)
                raise ValueError(message)

            normalize.append(row)
        except Exception as e:
            logger.error(f"Normalization failed: {e}")
            raise
    return normalize
