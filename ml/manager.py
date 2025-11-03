import os

import joblib
import pandas as pd

from config.config import logger

from .models.desicion_tree import train_reqression_model


class ModelManager:
    def __init__(self, model_name: str, model_path: str, encoder_path: str) -> None:
        """
        Initialize the ModelManager with model type and file paths.

        Args:
            model_name (str): Name of the model type (e.g., 'decision_tree').
            model_path (str): Path to save/load the trained model (.pkl).
            encoder_path (str): Path to save/load the fitted encoder (.pkl).

        Raises:
            ValueError: If the provided model_name is not supported.
        """
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
        """
        Check whether the saved model file exists on disk.

        Returns:
            bool: True if model file exists, False otherwise.
        """
        return os.path.exists(self.model_path)

    def load(self) -> None:
        """
        Load the trained model from disk into memory.

        Assumes that the model file exists at self.model_path.
        """
        self.model = joblib.load(self.model_path)

    def train(self, df: pd.DataFrame) -> None:
        """
        Train the model using the provided DataFrame and save artifacts.

        Args:
            df (pd.DataFrame): Preprocessed training data.

        Side Effects:
            - Trains model and encoder using the selected training function.
            - Saves model and encoder to disk at specified paths.
        """
        self.model, self.encoder = self.__train_fn(df)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.encoder, self.encoder_path)

    def get_or_train(self, df: pd.DataFrame) -> None:
        """
        Load the model from disk if it exists, otherwise train and save it.

        Args:
            df (pd.DataFrame): Preprocessed training data.
        """
        if self.model_exists():
            self.load()
        else:
            self.train(df)
