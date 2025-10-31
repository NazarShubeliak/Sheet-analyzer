from typing import List, Dict
import pandas as pd
from config.config import logger

def to_dataframe(data: List[Dict[str, str]]) -> pd.DataFrame:
    """
    Convert list of dicts to pandas DataFrame with proper types

    Args:
        data (List[Dict[str, str]]): Normalized data

    Returns:
        pd.DataFrame: Structured DataFrame
    """
    try:
        df = pd.DataFrame(data)
        df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
        logger.debug(f"Converted {len(df)} rows to DataFrame")
        return df
    except Exception as e:
        logger.error(f"Failed to convert to DataFrame: {e}")
        raise