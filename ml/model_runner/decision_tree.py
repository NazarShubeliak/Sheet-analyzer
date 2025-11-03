from datetime import datetime

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor


class Predictor:
    def __init__(self, model: DecisionTreeRegressor, encoder: LabelEncoder) -> None:
        """
        Initialize the Predictor with a trained model and fitted encoder.

        Args:
            model (DecisionTreeRegressor): Trained regression model for prediction.
            encoder (LabelEncoder): Fitted encoder for transforming country names.
        """
        self.model = model
        self.encoder = encoder

    def get_next_mount_date(self) -> str:
        """
        Compute the first day of the next calendar month.

        Returns:
            str: Date string in format 'YYYY-MM-DD' representing the next month.
        """ 
        next_mount = datetime.now().month + 1
        if next_mount > 12:
            next_mount = 1
        return f"2025-{next_mount:02d}-01"

    def build_input(self, df: pd.DataFrame, date_str: str) -> pd.DataFrame:
        """
        Build input DataFrame for prediction using unique countries and target date.

        Args:
            df (pd.DataFrame): Source DataFrame containing a 'Country' column.
            date_str (str): Target date string in format 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: DataFrame with columns 'Country', 'Date', 'Month', and 'Country_encoded'.
        """
        countries = df["Country"].unique()
        input_df = pd.DataFrame(
            {"Country": countries, "Date": [date_str] * len(countries)}
        )
        input_df["Month"] = pd.to_datetime(input_df["Date"]).dt.month
        input_df["Country_encoded"] = self.encoder.transform(input_df["Country"])
        return input_df

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate predictions using the model for the given input features.

        Args:
            df (pd.DataFrame): DataFrame with 'Country_encoded' and 'Month' columns.

        Returns:
            pd.DataFrame: Same DataFrame with an added 'Prediction' column.
        """
        x = df[["Country_encoded", "Month"]]
        df["Prediction"] = self.model.predict(x)
        return df

    def predict_next_month(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate predictions for all countries for the next calendar month.

        Args:
            df (pd.DataFrame): Source DataFrame containing historical 'Country' data.

        Returns:
            pd.DataFrame: DataFrame with predictions for each country in the next month.
        """
        date_str = self.get_next_mount_date()
        input_df = self.build_input(df, date_str)
        return self.predict(input_df)
