import joblib
import pandas as pd

from .manager import ModelManager
from .model_runner.decision_tree import Predictor
from config.config import logger


def run_model_pipeline(df: pd.DataFrame) -> None:
    """
    Train or load the decision tree model and generate predictions for the next calendar month.

    This function performs the following steps:
        1. Initializes a ModelManager for the decision tree model.
        2. Loads the model from disk if available, otherwise trains and saves it.
        3. Loads the fitted LabelEncoder from disk.
        4. Uses the Predictor class to generate country-level predictions for the next month.
        5. Prints the resulting DataFrame with predictions.

    Args:
        df (pd.DataFrame): Preprocessed dataset used for training and inference.
    """

    # Step 1: Create tree manager
    tree_manager = ModelManager(
        "decision_tree", r"ml\save_models\tree.pkl", r"ml\save_models\tree_encoder.pkl"
    )
    logger.Info(f"Create tree manager: {tree_manager.model_path}")

    # Step 2: Get or Train model
    tree_manager.get_or_train(df)
    logger.info(f"Get or train model")

    # Step 3: Load encoder for model
    encoder = joblib.load(r"ml\save_models\tree_encoder.pkl")
    logger.info(f"Get encoder: {tree_manager.encoder}")

    # Step 4: Uses the Predictor class to generate country-level predictions
    predictor = Predictor(tree_manager.model, encoder)
    result_df = predictor.predict_next_month(df)
    logger.info("Use the predictor class to generate country-level predicitons")

    # Step 5: Print result DataFrame
    print(result_df)
