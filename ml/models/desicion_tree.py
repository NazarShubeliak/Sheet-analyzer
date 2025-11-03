import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor

from config.config import logger


def train_reqression_model(df: pd.DataFrame) -> DecisionTreeRegressor:
    """
    Train a DecisionTreeRegressor to predict Total_EUR base on Country and Month

    Args:
        df (pd.DataFrame): Historical data with 'Country', 'Date', 'Total'

    Returns:
        DecisionTreeRegressor: Trained model
    """
    try:
        df = df.copy()
        df["Month"] = pd.to_datetime(df["Date"]).dt.month

        encoder = LabelEncoder()
        df["Country_encoded"] = encoder.fit_transform(df["Country"])

        x = df[["Country_encoded", "Month"]]
        y = df["Total"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        model = DecisionTreeRegressor(random_state=42)
        model.fit(x_train, y_train)

        score = model.score(x_test, y_test)
        logger.info(f"Model trained with R score: {score:.3f}")

        return model, encoder
    except Exception as e:
        logger.error(f"Failed to train reqression model: {e}")
        raise
