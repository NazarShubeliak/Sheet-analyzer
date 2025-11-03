import os

import joblib
import pandas as pd

from config.config import logger

from .models.desicion_tree import train_reqression_model


class ModelManager:
    def __init__(self, model_name: str, model_path: str, encoder_path: str) -> None:
        self.model_name = model_name
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model = None
        self.encoder = None

        self.__train_fn = {"decision_tree": train_reqression_model}.get(self.model_name)

        if self.__train_fn is None:
            message = f"Unknow model name {self.model_name}"
            logger.error(message)
            raise ValueError(message)

    def model_exists(self) -> bool:
        return os.path.exists(self.model_path)

    def load(self) -> None:
        self.model = joblib.load(self.model_path)

    def train(self, df: pd.DataFrame) -> None:
        self.model, self.encoder = self.__train_fn(df)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.encoder, self.encoder_path)

    def get_or_train(self, df: pd.DataFrame) -> None:
        if self.model_exists():
            self.load()
        else:
            self.train(df)
