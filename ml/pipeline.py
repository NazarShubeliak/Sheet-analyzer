import joblib
import pandas as pd

from .manager import ModelManager
from .model_runner.decision_tree import Predictor


def run_model_pipeline(df: pd.DataFrame) -> None:
    tree_mamanger = ModelManager(
        "decision_tree", r"ml\save_models\tree.pkl", r"ml\save_models\tree_encoder.pkl"
    )
    tree_mamanger.get_or_train(df)

    encoder = joblib.load(r"ml\save_models\tree_encoder.pkl")

    predictor = Predictor(tree_mamanger.model, encoder)
    result_df = predictor.predict_next_month(df)

    print(result_df)
