import pandas as pd

from .manager import ModelManager


def run_model_pipeline(df: pd.DataFrame) -> None:
    tree_mamanger = ModelManager("decision_tree", r"ml\save_models\tree.pkl")
    tree_mamanger.get_or_train(df)
