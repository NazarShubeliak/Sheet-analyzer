from datetime import datetime

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor


class Predictor:
    def __init__(self, model: DecisionTreeRegressor, encoder: LabelEncoder) -> None:
        self.model = model
        self.encoder = encoder

    def get_next_mount_date(self) -> str:
        next_mount = datetime.now().month + 1
        if next_mount > 12:
            next_mount = 1
        return f"2025-{next_mount:02d}-01"

    def build_input(self, df: pd.DataFrame, date_str: str) -> pd.DataFrame:
        countries = df["Country"].unique()
        input_df = pd.DataFrame(
            {"Country": countries, "Date": [date_str] * len(countries)}
        )
        input_df["Month"] = pd.to_datetime(input_df["Date"]).dt.month
        input_df["Country_encoded"] = self.encoder.transform(input_df["Country"])
        return input_df

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        x = df[["Country_encoded", "Month"]]
        df["Prediction"] = self.model.predict(x)
        return df

    def predict_next_month(self, df: pd.DataFrame) -> pd.DataFrame:
        date_str = self.get_next_mount_date()
        input_df = self.build_input(df, date_str)
        return self.predict(input_df)
